// Transform a canvas' first TH1 into a 2D histogram with pt on X and Counts on Y.
#include <algorithm>
#include <memory>
#include <vector>

#include "TAxis.h"
#include "TCanvas.h"
#include "TDirectory.h"
#include "TError.h"
#include "TFile.h"
#include "TIter.h"
#include "TKey.h"
#include "TList.h"
#include "TMath.h"
#include "TObject.h"
#include "TPad.h"
#include "TROOT.h"
#include "TH1.h"
#include "TH2D.h"
#include "TString.h"
#include "TSystem.h"

namespace {

TH1 *FindFirstHist(TPad *pad) {
  if (!pad) return nullptr;
  TIter next(pad->GetListOfPrimitives());
  TObject *obj = nullptr;
  while ((obj = next())) {
    if (obj->InheritsFrom(TH1::Class())) return static_cast<TH1 *>(obj);
    if (obj->InheritsFrom(TPad::Class())) {
      if (auto *h = FindFirstHist(static_cast<TPad *>(obj))) return h;
    }
  }
  return nullptr;
}

std::vector<double> ExtractEdges(const TAxis *axis) {
  const int nBins = axis->GetNbins();
  std::vector<double> edges(nBins + 1);
  const TArrayD *xbins = axis->GetXbins();
  if (xbins && xbins->GetSize() > 0) {
    for (int i = 0; i <= nBins; ++i) edges[i] = xbins->At(i);
  } else {
    for (int i = 1; i <= nBins; ++i) edges[i - 1] = axis->GetBinLowEdge(i);
    edges[nBins] = axis->GetBinUpEdge(nBins);
  }
  return edges;
}

}  // namespace

TH2D *CanvasToCountsVsPt(TCanvas *canvas,
                         const char *hist2DName = "h2_counts_vs_pt",
                         int nYBins = 200) {
  if (!canvas) {
    ::Error("CanvasToCountsVsPt", "Null canvas pointer");
    return nullptr;
  }
  auto *srcHist = FindFirstHist(canvas);
  if (!srcHist) {
    ::Error("CanvasToCountsVsPt", "No TH1 found on canvas '%s'",
            canvas->GetName());
    return nullptr;
  }

  const TAxis *xAxis = srcHist->GetXaxis();
  const int nXBins = xAxis->GetNbins();
  std::vector<double> xEdges = ExtractEdges(xAxis);

  const double yMax = std::max(srcHist->GetMaximum(), 1.0);
  const double yMin = 0.0;
  const double yHi = yMax * 1.2 + 1.0;
  if (nYBins < 1) nYBins = 1;

  auto *h2 = new TH2D(hist2DName,
                      Form("Counts vs p_{T} from %s;pt_binning;Counts",
                           srcHist->GetName()),
                      nXBins, xEdges.data(), nYBins, yMin, yHi);
  h2->SetDirectory(nullptr);
  h2->SetStats(false);

  for (int ix = 1; ix <= nXBins; ++ix) {
    const double xCenter = xAxis->GetBinCenter(ix);
    const double counts = srcHist->GetBinContent(ix);
    if (counts == 0.0) continue;
    const int iy = h2->GetYaxis()->FindBin(counts);
    h2->SetBinContent(h2->GetXaxis()->FindBin(xCenter), iy, counts);
  }

  return h2;
}

TH2D *CanvasToCountsVsPt(const char *canvasName,
                         const char *hist2DName = "h2_counts_vs_pt",
                         int nYBins = 200) {
  auto *canvas = dynamic_cast<TCanvas *>(gROOT->FindObject(canvasName));
  if (!canvas) {
    ::Error("CanvasToCountsVsPt", "Canvas '%s' not found", canvasName);
    return nullptr;
  }
  return CanvasToCountsVsPt(canvas, hist2DName, nYBins);
}

void canvas_to_hist2d(const char *canvasName = "c1") {
  TH2D *h2 = CanvasToCountsVsPt(canvasName);
  if (!h2) return;
  auto *c = new TCanvas(Form("c_%s_to_h2", canvasName),
                        "Counts vs pt (2D)", 900, 650);
  h2->Draw("COLZ");
  c->Update();
}

namespace {

void ConvertDirectoryToHist2D(TDirectory *dir,
                              std::vector<TH2D *> &outHists,
                              TFile *outFile,
                              int nYBins) {
  if (!dir) return;

  TIter next(dir->GetListOfKeys());
  TKey *key = nullptr;
  while ((key = static_cast<TKey *>(next()))) {
    TObject *obj = key->ReadObj();
    if (!obj) continue;

    if (obj->InheritsFrom(TDirectory::Class())) {
      ConvertDirectoryToHist2D(static_cast<TDirectory *>(obj), outHists,
                               outFile, nYBins);
      continue;
    }

    if (!obj->InheritsFrom(TCanvas::Class())) continue;

    auto *canvas = static_cast<TCanvas *>(obj);
    TString h2Name = Form("%s_h2", canvas->GetName());
    TH2D *h2 = CanvasToCountsVsPt(canvas, h2Name, nYBins);
    if (!h2) continue;

    outHists.push_back(h2);
    if (outFile) {
      outFile->cd();
      h2->SetDirectory(outFile);
      h2->Write();
    }
  }
}

}  // namespace

std::vector<TH2D *> canvases_in_file_to_hist2d(const char *inputFile,
                                               const char *outputFile = "",
                                               int nYBins = 200) {
  std::vector<TH2D *> converted;
  std::unique_ptr<TFile> inFile(TFile::Open(inputFile, "READ"));
  if (!inFile || inFile->IsZombie()) {
    ::Error("canvases_in_file_to_hist2d", "Could not open '%s'", inputFile);
    return converted;
  }

  TString outName = outputFile;
  if (!outName.Length()) {
    outName = gSystem->BaseName(inputFile);
    outName += "_h2";
    if (!outName.EndsWith(".root")) outName += ".root";
  }

  std::unique_ptr<TFile> outFile(TFile::Open(outName, "RECREATE"));
  if (!outFile || outFile->IsZombie()) {
    ::Warning("canvases_in_file_to_hist2d",
              "Will not write output file (failed to create '%s')",
              outName.Data());
    outFile.reset();
  }

  ConvertDirectoryToHist2D(inFile.get(), converted, outFile.get(), nYBins);

  if (outFile) {
    outFile->Write();
    outFile->Close();
  }

  return converted;
}

void file_canvases_to_hist2d(const char *inputFile,
                             const char *outputFile = "",
                             int nYBins = 200) {
  auto hists = canvases_in_file_to_hist2d(inputFile, outputFile, nYBins);
  ::Info("file_canvases_to_hist2d",
         "Converted %zu canvases from '%s' into 2D histograms", hists.size(),
         inputFile);
}
