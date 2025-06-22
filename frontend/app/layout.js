
import { Inter } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/sonner.jsx";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Geo-AI Visualizer",
  description: "Ask the Map a question",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        
        <link
          rel="stylesheet"
          href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
          integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
          crossOrigin=""
        />
      </head>
      <body className={inter.className}>
        {children}
        <Toaster richColors />
      </body>
    </html>
  );
}