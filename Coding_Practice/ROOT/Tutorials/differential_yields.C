// Build differential yield spectra for reco and truth, overlaying 0-30 and
// 60-100 centralities. Produces histograms, graphs, and canvases in one ROOT
// file. Input files can be provided as lists (one per centrality); the macro
// searches for a TH2 (uses ProjectionX) or TH1 if a name is not provided.
#include <algorithm>
#include <memory>
#include <string>
#include <vector>

#include "TCanvas.h"
#include "TColor.h"
#include "TDirectory.h"
#include "TError.h"
#include "TFile.h"
#include "TGraphErrors.h"
#include "TH1.h"
#include "TH1D.h"
#include "TH2.h"
#include "TKey.h"
#include "TLegend.h"
#include "TList.h"
#include "TROOT.h"

namespace {

struct PtSummary {
  TH1D *counts = nullptr;
  TH1D *density = nullptr;
};

struct InputSpec {
  TString file;
  TString histName;  // optional: if empty, first TH2 (or TH1) is used
  TString label;     // legend label
  TString tag;       // tag for naming outputs
};

TString Sanitize(const TString &s) {
  TString out(s);
  out.ReplaceAll(" ", "_");
  out.ReplaceAll("%", "pct");
  out.ReplaceAll("-", "_");
  out.ReplaceAll("/", "_");
  return out;
}

TH2 *FindFirstTH2(TDirectory *dir) {
  if (!dir) return nullptr;
  TIter next(dir->GetListOfKeys());
  TKey *key = nullptr;
  while ((key = static_cast<TKey *>(next()))) {
    TObject *obj = key->ReadObj();
    if (!obj) continue;
    if (obj->InheritsFrom(TH2::Class())) return static_cast<TH2 *>(obj);
    if (obj->InheritsFrom(TDirectory::Class())) {
      if (auto *h2 = FindFirstTH2(static_cast<TDirectory *>(obj))) return h2;
    }
  }
  return nullptr;
}

TH1 *FindFirstTH1(TDirectory *dir) {
  if (!dir) return nullptr;
  TIter next(dir->GetListOfKeys());
  TKey *key = nullptr;
  while ((key = static_cast<TKey *>(next()))) {
    TObject *obj = key->ReadObj();
    if (!obj) continue;
    if (obj->InheritsFrom(TH1::Class())) return static_cast<TH1 *>(obj);
    if (obj->InheritsFrom(TDirectory::Class())) {
      if (auto *h1 = FindFirstTH1(static_cast<TDirectory *>(obj))) return h1;
    }
  }
  return nullptr;
}

TH1 *LoadPtHistogram(const InputSpec &spec) {
  std::unique_ptr<TFile> fin(TFile::Open(spec.file, "READ"));
  if (!fin || fin->IsZombie()) {
    ::Error("LoadPtHistogram", "Cannot open %s", spec.file.Data());
    return nullptr;
  }

  TObject *obj = nullptr;
  if (spec.histName.Length()) obj = fin->Get(spec.histName);
  if (!obj) obj = FindFirstTH2(fin.get());
  if (!obj) obj = FindFirstTH1(fin.get());

  TH1 *hOut = nullptr;
  if (obj && obj->InheritsFrom(TH2::Class())) {
    auto *h2 = static_cast<TH2 *>(obj);
    TString projName = Form("%s_px", h2->GetName());
    TH1 *proj = h2->ProjectionX(projName, 1, -1, "e");
    proj->SetDirectory(nullptr);
    hOut = proj;
  } else if (obj && obj->InheritsFrom(TH1::Class())) {
    auto *h1 = static_cast<TH1 *>(obj);
    hOut = static_cast<TH1 *>(h1->Clone(Form("%s_clone", h1->GetName())));
    hOut->SetDirectory(nullptr);
  } else {
    ::Error("LoadPtHistogram",
            "No suitable TH2/TH1 found in %s (requested '%s')",
            spec.file.Data(), spec.histName.Data());
  }

  return hOut;
}

PtSummary IntegratePtBins(TH1 *h,
                          const std::vector<double> &ptEdges,
                          const char *tag) {
  PtSummary res;
  if (!h) {
    ::Error("IntegratePtBins", "Null input hist");
    return res;
  }
  if (ptEdges.size() < 2) {
    ::Error("IntegratePtBins", "Need at least two pT edges");
    return res;
  }

  const int nBins = ptEdges.size() - 1;
  TString countsName = Form("counts_%s", tag);
  TString densityName = Form("density_%s", tag);
  res.counts = new TH1D(countsName, "Counts per p_{T};p_{T};Counts",
                        nBins, ptEdges.data());
  res.density = new TH1D(
      densityName, "dN/dp_{T};p_{T};dN/dp_{T} [GeV^{-1}]",
      nBins, ptEdges.data());
  res.counts->SetDirectory(nullptr);
  res.density->SetDirectory(nullptr);

  for (int i = 0; i < nBins; ++i) {
    const double low = ptEdges[i];
    const double high = ptEdges[i + 1];
    int bin1 = h->GetXaxis()->FindBin(low);
    int bin2 = h->GetXaxis()->FindBin(high * (1.0 - 1e-9));
    bin1 = std::max(bin1, 1);
    bin2 = std::min(bin2, h->GetNbinsX());

    double err = 0.0;
    const double counts = h->IntegralAndError(bin1, bin2, err);
    const double width = high - low;
    const double density = (width > 0) ? counts / width : 0.0;
    const double densityErr = (width > 0) ? err / width : 0.0;

    res.counts->SetBinContent(i + 1, counts);
    res.counts->SetBinError(i + 1, err);
    res.density->SetBinContent(i + 1, density);
    res.density->SetBinError(i + 1, densityErr);
  }

  return res;
}

TGraphErrors *MakeGraph(const TH1D *h, const char *name,
                        int color, int marker) {
  if (!h) return nullptr;
  const int n = h->GetNbinsX();
  auto *g = new TGraphErrors(n);
  g->SetName(name);
  g->SetTitle(h->GetTitle());
  for (int i = 0; i < n; ++i) {
    const double x = h->GetXaxis()->GetBinCenter(i + 1);
    const double ex = h->GetXaxis()->GetBinWidth(i + 1) * 0.5;
    const double y = h->GetBinContent(i + 1);
    const double ey = h->GetBinError(i + 1);
    g->SetPoint(i, x, y);
    g->SetPointError(i, ex, ey);
  }
  g->SetMarkerColor(color);
  g->SetLineColor(color);
  g->SetMarkerStyle(marker);
  g->SetLineWidth(2);
  return g;
}

void DrawSpectra(const char *canvasName,
                 const char *title,
                 const std::vector<TGraphErrors *> &graphs,
                 const std::vector<TString> &labels) {
  if (graphs.empty()) return;
  auto *c = new TCanvas(canvasName, title, 900, 700);
  c->SetGrid();

  TLegend *leg = new TLegend(0.6, 0.65, 0.88, 0.88);
  leg->SetBorderSize(0);

  bool first = true;
  for (size_t i = 0; i < graphs.size(); ++i) {
    auto *g = graphs[i];
    if (!g) continue;
    if (first) {
      g->Draw("AP");
      g->GetHistogram()->GetYaxis()->SetTitle("dN/dp_{T} [GeV^{-1}]");
      g->GetHistogram()->GetXaxis()->SetTitle("p_{T} [GeV]");
      first = false;
    } else {
      g->Draw("P SAME");
    }
    if (i < labels.size()) leg->AddEntry(g, labels[i], "lp");
  }

  leg->Draw();
  c->Update();
}

}  // namespace

void make_differential_yields(
    std::vector<std::string> recoFiles = std::vector<std::string>(),
    std::vector<std::string> truthFiles = std::vector<std::string>(),
    std::vector<std::string> recoHists = std::vector<std::string>(),
    std::vector<std::string> truthHists = std::vector<std::string>(),
    std::vector<std::string> centLabels = std::vector<std::string>(),
    const char *outRoot = "differential_yields.root",
    std::vector<double> ptEdges = std::vector<double>{1, 2, 3, 4, 5, 6, 7}) {
  if (ptEdges.size() < 2) {
    ::Error("make_differential_yields", "Need at least two pT edges");
    return;
  }
  if (recoFiles.empty() || truthFiles.empty()) {
    ::Error("make_differential_yields", "Provide at least one reco and truth file");
    return;
  }

  const int colors[] = {kAzure + 1, kBlue + 1, kOrange + 7, kRed + 1,
                        kGreen + 2, kViolet + 1};
  const int markers[] = {20, 21, 22, 23, 24, 25};

  auto buildSpecs = [&](const std::vector<std::string> &files,
                        const std::vector<std::string> &hists,
                        const std::vector<std::string> &labels,
                        const char *prefix) {
    std::vector<InputSpec> specs;
    for (size_t i = 0; i < files.size(); ++i) {
      InputSpec spec;
      spec.file = files[i].c_str();
      if (i < hists.size()) spec.histName = hists[i].c_str();
      TString lab =
          (i < labels.size()) ? labels[i].c_str() : Form("entry_%zu", i);
      spec.label = Form("%s %s", prefix, lab.Data());
      spec.tag = Sanitize(Form("%s_%s", prefix, lab.Data()));
      specs.push_back(spec);
    }
    return specs;
  };

  auto recoSpecs = buildSpecs(recoFiles, recoHists, centLabels, "Reco");
  auto truthSpecs = buildSpecs(truthFiles, truthHists, centLabels, "Truth");

  std::vector<PtSummary> recoSummaries;
  std::vector<PtSummary> truthSummaries;
  std::vector<TGraphErrors *> gReco;
  std::vector<TGraphErrors *> gTruth;
  std::vector<TString> recoLabels;
  std::vector<TString> truthLabels;

  auto process = [&](const std::vector<InputSpec> &specs,
                     std::vector<PtSummary> &outSummaries,
                     std::vector<TGraphErrors *> &outGraphs,
                     std::vector<TString> &outLabels,
                     const char *prefix) {
    for (size_t i = 0; i < specs.size(); ++i) {
      const auto &spec = specs[i];
      std::unique_ptr<TH1> h(LoadPtHistogram(spec));
      if (!h) continue;
      PtSummary ps = IntegratePtBins(h.get(), ptEdges, spec.tag);
      if (!ps.density) continue;
      outSummaries.push_back(ps);
      int color = colors[i % (sizeof(colors) / sizeof(int))];
      int marker = markers[i % (sizeof(markers) / sizeof(int))];
      TString gname = Form("g_%s_%s", prefix, spec.tag.Data());
      TGraphErrors *g =
          MakeGraph(ps.density, gname, color, marker);
      outGraphs.push_back(g);
      outLabels.push_back(spec.label);
    }
  };

  process(recoSpecs, recoSummaries, gReco, recoLabels, "reco");
  process(truthSpecs, truthSummaries, gTruth, truthLabels, "truth");

  TFile *fOut = TFile::Open(outRoot, "RECREATE");
  if (!fOut || fOut->IsZombie()) {
    ::Error("make_differential_yields", "Cannot create %s", outRoot);
    return;
  }

  for (const auto &ps : recoSummaries) {
    if (ps.counts) ps.counts->Write();
    if (ps.density) ps.density->Write();
  }
  for (const auto &ps : truthSummaries) {
    if (ps.counts) ps.counts->Write();
    if (ps.density) ps.density->Write();
  }

  DrawSpectra("c_reco_dNdpt", "Reco dN/dp_{T}", gReco, recoLabels);
  DrawSpectra("c_truth_dNdpt", "Truth dN/dp_{T}", gTruth, truthLabels);

  fOut->cd();
  for (auto *g : gReco) {
    if (g) g->Write();
  }
  for (auto *g : gTruth) {
    if (g) g->Write();
  }

  if (auto *cReco =
          dynamic_cast<TCanvas *>(gROOT->FindObject("c_reco_dNdpt"))) {
    cReco->Write();
  }
  if (auto *cTruth =
          dynamic_cast<TCanvas *>(gROOT->FindObject("c_truth_dNdpt"))) {
    cTruth->Write();
  }

  fOut->Close();
}
