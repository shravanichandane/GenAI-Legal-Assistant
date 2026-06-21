"use client";

import React, { useState, useEffect } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import "react-pdf/dist/esm/Page/AnnotationLayer.css";
import "react-pdf/dist/esm/Page/TextLayer.css";

// Set up the worker for pdfjs
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

interface BoundingBox {
  x0: number;
  top: number;
  x1: number;
  bottom: number;
  pageNumber: number;
}

interface Risk {
  id: string;
  boundingBox?: BoundingBox;
}

interface PdfViewerProps {
  url: string;
  zoom: number; // 100 = 1.0 scale
  risks: Risk[];
  activeRiskId: string | null;
}

export default function PdfViewer({ url, zoom, risks, activeRiskId }: PdfViewerProps) {
  const [numPages, setNumPages] = useState<number | null>(null);

  const scale = zoom / 100;

  function onDocumentLoadSuccess({ numPages }: { numPages: number }) {
    setNumPages(numPages);
  }

  // Find the risk that is currently active, to scroll to it or highlight it specially
  const activeRisk = risks.find(r => r.id === activeRiskId);

  // We want to render a box for each risk. If activeRisk is set, highlight it more.
  const renderOverlays = (pageIndex: number) => {
    // pageIndex is 1-based to match pdfplumber pageNumber
    const pageRisks = risks.filter(r => r.boundingBox && r.boundingBox.pageNumber === pageIndex);

    return pageRisks.map(risk => {
      const box = risk.boundingBox!;
      const isActive = risk.id === activeRiskId;
      
      const style: React.CSSProperties = {
        position: "absolute",
        left: `${box.x0 * scale}px`,
        top: `${box.top * scale}px`,
        width: `${(box.x1 - box.x0) * scale}px`,
        height: `${(box.bottom - box.top) * scale}px`,
        backgroundColor: isActive ? "rgba(217, 119, 6, 0.4)" : "rgba(217, 119, 6, 0.15)", // amber-600 with opacity
        border: isActive ? "2px solid rgba(217, 119, 6, 1)" : "1px solid rgba(217, 119, 6, 0.5)",
        cursor: "pointer",
        zIndex: 10,
        transition: "all 0.3s ease",
        borderRadius: "2px",
        pointerEvents: "none" // Let clicks pass through if needed, or handle clicks to activate
      };

      return <div key={risk.id} style={style} className={isActive ? "ring-2 ring-amber-500 ring-offset-2" : ""} />;
    });
  };

  return (
    <div className="flex flex-col items-center">
      <Document
        file={url}
        options={{ withCredentials: true }}
        onLoadSuccess={onDocumentLoadSuccess}
        loading={
          <div className="flex items-center justify-center p-20 text-slate-400 font-mono text-sm">
            Loading document securely...
          </div>
        }
        error={
          <div className="flex items-center justify-center p-20 text-rose-500 font-mono text-sm">
            Failed to load PDF document.
          </div>
        }
      >
        {numPages && Array.from(new Array(numPages), (el, index) => (
          <div key={`page_${index + 1}`} className="mb-8 relative shadow-xl border border-slate-200">
            <Page
              pageNumber={index + 1}
              scale={scale}
              renderTextLayer={true}
              renderAnnotationLayer={true}
              className="bg-white"
            />
            {/* Overlay Container */}
            <div className="absolute inset-0 pointer-events-none">
              {renderOverlays(index + 1)}
            </div>
          </div>
        ))}
      </Document>
    </div>
  );
}
