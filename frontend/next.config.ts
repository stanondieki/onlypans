import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options for local development */
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  },
};

export default nextConfig;
