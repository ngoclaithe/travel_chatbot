'use client';

import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Compass, MapPin, Users, Utensils } from 'lucide-react';

const features = [
  {
    icon: MapPin,
    title: 'Khám Phá Điểm Đến',
    description: 'Khám phá những điểm đến du lịch tuyệt vời trên khắp thế giới',
    href: '/destinations',
  },
  {
    icon: Compass,
    title: 'Tìm Tour Du Lịch',
    description: 'Duyệt qua các gói tour được lựa chọn cẩn thận cho những trải nghiệm không thể quên',
    href: '/tours',
  },
  {
    icon: Users,
    title: 'Đặt Khách Sạn',
    description: 'Tìm nơi ở lý tưởng từ danh sách khách sạn của chúng tôi',
    href: '/hotels',
  },
  {
    icon: Utensils,
    title: 'Khám Phá Nhà Hàng',
    description: 'Thưởng thức ẩm thực địa phương tại các nhà hàng được khuyến nghị',
    href: '/restaurants',
  },
];

export default function Home() {
  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-ocean-blue to-ocean-light text-white py-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            Trợ Lý Du Lịch Thông Minh Của Bạn 🌍
          </h1>
          <p className="text-xl md:text-2xl mb-8 opacity-90">
            Khám phá, lên kế hoạch và đặt chuyến du lịch hoàn hảo của bạn với Travelbot
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/destinations">
              <Button
                size="lg"
                className="bg-sand-yellow text-white hover:bg-sand-light font-semibold"
              >
                Bắt Đầu Khám Phá
              </Button>
            </Link>
            <Link href="/about">
              <Button
                size="lg"
                className="bg-sand-yellow text-white hover:bg-sand-light font-semibold"
              >
                Tìm Hiểu Thêm
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-white dark:bg-background">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">
            Khám Phá Cùng Travelbot
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature) => {
              const Icon = feature.icon;
              return (
                <Link key={feature.href} href={feature.href}>
                  <Card className="h-full hover:shadow-lg transition-shadow cursor-pointer border-2 border-transparent hover:border-ocean-blue">
                    <CardHeader>
                      <div className="w-12 h-12 rounded-lg bg-ocean-light/10 flex items-center justify-center mb-4">
                        <Icon className="w-6 h-6 text-ocean-blue" />
                      </div>
                      <CardTitle>{feature.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <CardDescription>{feature.description}</CardDescription>
                    </CardContent>
                  </Card>
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-ocean-blue/5 py-16 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">Sẵn Sàng Lên Kế Hoạch Chuyến Du Lịch?</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-8 max-w-2xl mx-auto">
            Sử dụng chatbot AI của chúng tôi để nhận các gợi ý du lịch được cá nhân hóa,
            đặt khách sạn và tour du lịch, và lên kế hoạch cho chuyến đi hoàn hảo.
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            💬 Bắt đầu trò chuyện với trợ lý AI của chúng tôi ở góc dưới cùng bên phải
          </p>
        </div>
      </section>
    </div>
  );
}
