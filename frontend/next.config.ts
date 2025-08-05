import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  images: {
    unoptimized: true,
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://onlypans.onrender.com/api',
  },
  // Enable experimental features for better Vercel compatibility
  experimental: {
    esmExternals: true,
  },
};

export default nextConfig;
