import type { NextConfig } from "next";

// In GitHub Actions this is set to /<repo-name> so all assets resolve correctly.
// Locally it stays empty so localhost works without a sub-path.
const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";

const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
  images: { unoptimized: true },
  basePath,
  // assetPrefix mirrors basePath so JS/CSS chunks are fetched from the right path
  assetPrefix: basePath,
};

export default nextConfig;
