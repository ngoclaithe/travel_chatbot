'use client';

import React from 'react';
import Image from 'next/image';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Tour } from '@/types';
import { MapPin, Calendar } from 'lucide-react';

interface TourCardProps {
  tour: Tour;
}

export const TourCard: React.FC<TourCardProps> = ({ tour }) => {
  const formatDestinations = (d: any) => {
    if (!d) return '';

    let processed = d;
    // 1. Try to parse if strictly a string
    if (typeof d === 'string') {
      try {
        if (d.trim().startsWith('[') || d.trim().startsWith('{')) {
          processed = JSON.parse(d);
        }
      } catch (e) {
        // Keep as string
      }
    }

    if (typeof processed === 'string') return processed;

    // 2. Handle object (single destination)
    if (!Array.isArray(processed) && typeof processed === 'object' && processed !== null) {
      return processed.name || processed.title || String(processed);
    }

    // 3. Handle Array
    if (Array.isArray(processed)) {
      return processed
        .map((item) => {
          if (typeof item === 'string') {
            // Check if the item ITSELF is a JSON string
            try {
              if (item.trim().startsWith('{') || item.trim().startsWith('[')) {
                const parsedItem = JSON.parse(item);
                if (Array.isArray(parsedItem)) {
                  return parsedItem.map((sub: any) => sub.name || sub.title || sub).join(', ');
                }
                if (typeof parsedItem === 'object' && parsedItem !== null) {
                  return parsedItem.name || parsedItem.title || String(parsedItem);
                }
              }
            } catch { }
            return item;
          }
          if (typeof item === 'object' && item !== null) {
            return item.name || item.title || String(item);
          }
          return String(item);
        })
        .join(', ');
    }

    return String(processed);
  };

  return (
    <Card className="overflow-hidden hover:shadow-lg transition-shadow h-full">
      {tour.image_url && (
        <div className="w-full h-48 bg-gray-200 dark:bg-gray-700 overflow-hidden relative">
          <Image
            src={tour.image_url}
            alt={tour.name}
            fill
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            className="object-cover hover:scale-105 transition-transform"
            unoptimized
          />
        </div>
      )}
      <CardHeader className="pb-3">
        <CardTitle className="text-lg">{tour.name}</CardTitle>
        <CardDescription className="flex items-center gap-1">
          <MapPin className="w-4 h-4" />
          {formatDestinations(tour.destinations)}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
          {tour.description}
        </p>
        <div className="space-y-2 pt-3 border-t border-border">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm">
              <Calendar className="w-4 h-4 text-ocean-blue" />
              <span>
                {tour.duration_days
                  ? `${tour.duration_days} ngày`
                  : 'Không rõ thời lượng'}
              </span>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600 dark:text-gray-400">
              Giá mỗi người:
            </span>
            <span className="flex items-center gap-1 font-semibold text-sand-yellow text-lg">
              {tour.price ? `${Number(tour.price).toLocaleString('vi-VN')} VNĐ` : 'Liên hệ'}
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
