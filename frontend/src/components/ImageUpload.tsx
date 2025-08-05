'use client';

import React, { useState, useCallback } from 'react';
import Image from 'next/image';
import { useDropzone } from 'react-dropzone';
import { Upload, Camera, Loader2 } from 'lucide-react';
import { recipeAPI } from '@/lib/api';

interface GeneratedRecipe {
  name: string;
  description: string;
  ingredients: Array<{ name: string; amount: string; unit: string }>;
  instructions: string[];
  prep_time: number;
  cook_time: number;
  servings: number;
  difficulty: string;
}

interface ImageUploadProps {
  onRecipeGenerated: (recipe: GeneratedRecipe) => void;
}

export default function ImageUpload({ onRecipeGenerated }: ImageUploadProps) {
  const [loading, setLoading] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    // Create preview
    const previewUrl = URL.createObjectURL(file);
    setPreview(previewUrl);
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('image', file);
      
      const response = await recipeAPI.identifyFood(formData);
      onRecipeGenerated(response.data);
    } catch (error) {
      console.error('Error identifying food:', error);
    } finally {
      setLoading(false);
    }
  }, [onRecipeGenerated]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp']
    },
    maxFiles: 1
  });

  return (
    <div className="w-full max-w-md mx-auto">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
          ${loading ? 'pointer-events-none opacity-50' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        {loading ? (
          <Loader2 className="w-12 h-12 mx-auto mb-4 animate-spin text-blue-500" />
        ) : (
          <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
        )}
        
        <h3 className="text-lg font-medium mb-2">
          {loading ? 'Analyzing image...' : 'Upload food image'}
        </h3>
        
        <p className="text-gray-500 mb-4">
          Drop an image here or click to browse
        </p>
        
        <button
          type="button"
          className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          disabled={loading}
        >
          <Camera className="w-4 h-4 mr-2" />
          Choose Image
        </button>
      </div>
      
      {preview && (
        <div className="mt-4">
          <Image
            src={preview}
            alt="Preview"
            width={400}
            height={192}
            className="w-full h-48 object-cover rounded-lg"
          />
        </div>
      )}
    </div>
  );
}
