'use client';

import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { AdminLayout } from '@/components/admin/AdminLayout';
import axiosClient from '@/lib/axiosClient';
import { ApiResponse } from '@/types';
import { BarChart3, Users, MapPin, Hotel, Compass } from 'lucide-react';

interface DashboardStats {
  destinations_count: number;
  hotels_count: number;
  tours_count: number;
  restaurants_count: number;
  activities_count: number;
  reviews_count: number;
}

const StatCard: React.FC<{
  icon: React.ReactNode;
  label: string;
  value: number | string;
  color: string;
}> = ({ icon, label, value, color }) => (
  <Card className="border-none shadow-sm">
    <CardContent className="pt-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-muted-foreground">{label}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
        </div>
        <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${color}`}>
          {icon}
        </div>
      </div>
    </CardContent>
  </Card>
);

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setIsLoading(true);

      const [destinationsRes, hotelsRes, toursRes, restaurantsRes, activitiesRes, reviewsRes] =
        await Promise.all([
          axiosClient.get<ApiResponse<unknown[]>>('/destinations/'),
          axiosClient.get<ApiResponse<unknown[]>>('/hotels/'),
          axiosClient.get<ApiResponse<unknown[]>>('/tours/'),
          axiosClient.get<ApiResponse<unknown[]>>('/restaurants/'),
          axiosClient.get<ApiResponse<unknown[]>>('/activities/'),
          axiosClient.get<ApiResponse<unknown[]>>('/reviews/'),
        ]).catch((error) => {
          console.error('Failed to fetch stats:', error);
          return [
            { data: { data: [] } },
            { data: { data: [] } },
            { data: { data: [] } },
            { data: { data: [] } },
            { data: { data: [] } },
            { data: { data: [] } },
          ];
        });

      setStats({
        destinations_count: destinationsRes.data.data?.length || 0,
        hotels_count: hotelsRes.data.data?.length || 0,
        tours_count: toursRes.data.data?.length || 0,
        restaurants_count: restaurantsRes.data.data?.length || 0,
        activities_count: activitiesRes.data.data?.length || 0,
        reviews_count: reviewsRes.data.data?.length || 0,
      });
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AdminLayout>
      <div>
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Bảng Điều Khiển
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Chào mừng quay lại! Đây là tổng quan về dữ liệu du lịch của bạn.
          </p>

        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array.from({ length: 6 }).map((_, i) => (
              <Card key={i} className="animate-pulse">
                <CardContent className="pt-6">
                  <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded mb-4" />
                  <div className="h-12 bg-gray-200 dark:bg-gray-700 rounded" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : stats ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <StatCard
              icon={<MapPin className="w-6 h-6 text-white" />}
              label="Điểm Đến"
              value={stats.destinations_count}
              color="bg-ocean-blue"
            />
            <StatCard
              icon={<Hotel className="w-6 h-6 text-white" />}
              label="Khách Sạn"
              value={stats.hotels_count}
              color="bg-sand-yellow text-dark-gray"
            />
            <StatCard
              icon={<Compass className="w-6 h-6 text-white" />}
              label="Tour Du Lịch"
              value={stats.tours_count}
              color="bg-accent"
            />
            <StatCard
              icon={<Users className="w-6 h-6 text-white" />}
              label="Nhà Hàng"
              value={stats.restaurants_count}
              color="bg-green-500"
            />
            <StatCard
              icon={<BarChart3 className="w-6 h-6 text-white" />}
              label="Hoạt Động"
              value={stats.activities_count}
              color="bg-purple-500"
            />
            <StatCard
              icon={<Users className="w-6 h-6 text-white" />}
              label="Bình Luận"
              value={stats.reviews_count}
              color="bg-indigo-500"
            />
          </div>
        ) : (
          <Card>
            <CardContent className="pt-6">
              <p className="text-muted-foreground">
                Không thể tải thống kê. Vui lòng thử lại sau.
              </p>
            </CardContent>
          </Card>
        )}

        {/* Quick Actions */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Hành Động Nhanh</CardTitle>
            <CardDescription>
              Quản lý dữ liệu du lịch của bạn một cách nhanh chóng và hiệu quả
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <a
                href="/admin/destinations"
                className="p-4 bg-blue-50 dark:bg-blue-950/20 rounded-lg border border-blue-200 dark:border-blue-800 hover:shadow-md transition-shadow text-center"
              >
                <p className="font-semibold text-blue-900 dark:text-blue-100">
                  Quản Lý Điểm Đến
                </p>
              </a>
              <a
                href="/admin/hotels"
                className="p-4 bg-amber-50 dark:bg-amber-950/20 rounded-lg border border-amber-200 dark:border-amber-800 hover:shadow-md transition-shadow text-center"
              >
                <p className="font-semibold text-amber-900 dark:text-amber-100">
                  Quản Lý Khách Sạn
                </p>
              </a>
              <a
                href="/admin/tours"
                className="p-4 bg-cyan-50 dark:bg-cyan-950/20 rounded-lg border border-cyan-200 dark:border-cyan-800 hover:shadow-md transition-shadow text-center"
              >
                <p className="font-semibold text-cyan-900 dark:text-cyan-100">
                  Quản Lý Tour Du Lịch
                </p>
              </a>
            </div>
          </CardContent>
        </Card>
      </div>
    </AdminLayout>
  );
}
