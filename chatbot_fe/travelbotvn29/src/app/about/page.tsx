'use client';

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { CheckCircle, Zap, Users, Globe } from 'lucide-react';

const features = [
  {
    icon: Zap,
    title: 'Hỗ Trợ AI',
    description: 'Chatbot thông minh của chúng tôi cung cấp gợi ý du lịch cá nhân hóa 24/7',
  },
  {
    icon: Globe,
    title: 'Phạm Vi Toàn Cầu',
    description: 'Khám phá các điểm đến trên khắp thế giới với dữ liệu du lịch toàn diện',
  },
  {
    icon: Users,
    title: 'Cộng Đồng Dẫn Dắt',
    description: 'Hưởng lợi từ các đánh giá thực tế và gợi ý từ các du khách khác',
  },
  {
    icon: CheckCircle,
    title: 'Đặt Phòng Dễ Dàng',
    description: 'Đặt phòng khách sạn, tour du lịch và khám phá nhà hàng t��i một nơi',
  },
];

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-white dark:bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-ocean-blue to-ocean-light text-white py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold mb-4">Về Du Lịch AI</h1>
          <p className="text-xl opacity-90">
            Trợ lý du lịch được hỗ trợ bởi AI cho những chuyến du lịch không thể quên
          </p>
        </div>
      </div>

      {/* Mission Section */}
      <section className="max-w-4xl mx-auto px-4 py-16">
        <div className="grid md:grid-cols-2 gap-12 items-center mb-16">
          <div>
            <h2 className="text-4xl font-bold mb-6">Sứ Mệnh Của Chúng Tôi</h2>
            <p className="text-lg text-gray-700 dark:text-gray-300 mb-4">
              Tại Du Lịch AI, chúng tôi tin rằng du lịch nên dễ tiếp cận, được cá nhân hóa và
              không thể quên. Sứ mệnh của chúng tôi là trao quyền cho các du khách với các công cụ thông minh và
              thông tin toàn diện để lên kế hoạch và đặt chuyến du lịch hoàn hảo của họ.
            </p>
            <p className="text-lg text-gray-700 dark:text-gray-300">
              Chúng tôi sử dụng công nghệ AI tiên tiến để cung cấp các gợi ý được cá nhân hóa,
              các tùy chọn đặt phòng theo thời gian thực, và những hiểu biết du lịch của chuyên gia được điều chỉnh theo
              sở thích và nhu cầu độc đáo của bạn.
            </p>
          </div>
          <div className="bg-gradient-to-br from-ocean-light to-accent rounded-lg p-12 text-white">
            <div className="text-center">
              <Globe className="w-24 h-24 mx-auto mb-4 opacity-80" />
              <h3 className="text-2xl font-bold">Khám Phá Thế Giới</h3>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-gray-50 dark:bg-dark-gray/50 py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">Tại Sao Chọn Du Lịch AI?</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature) => {
              const Icon = feature.icon;
              return (
                <Card key={feature.title} className="border-none shadow-sm">
                  <CardHeader>
                    <div className="w-12 h-12 rounded-lg bg-ocean-blue/10 flex items-center justify-center mb-4">
                      <Icon className="w-6 h-6 text-ocean-blue" />
                    </div>
                    <CardTitle className="text-lg">{feature.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription>{feature.description}</CardDescription>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="max-w-4xl mx-auto px-4 py-16">
        <h2 className="text-4xl font-bold mb-12 text-center">Các Giá Trị Của Chúng Tôi</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-blue-50 dark:bg-blue-950/20 p-8 rounded-lg">
            <h3 className="text-2xl font-semibold mb-3 text-ocean-blue">Đổi Mới</h3>
            <p className="text-gray-700 dark:text-gray-300">
              Chúng tôi liên tục đổi mới để mang đến cho bạn công nghệ AI và giải pháp du lịch mới nhất.
            </p>
          </div>

          <div className="bg-amber-50 dark:bg-amber-950/20 p-8 rounded-lg">
            <h3 className="text-2xl font-semibold mb-3 text-sand-yellow">Độ Tin Cậy</h3>
            <p className="text-gray-700 dark:text-gray-300">
              Lòng tin là cốt lõi của mọi thứ chúng tôi làm. Chúng tôi đảm bảo thông tin du lịch chính xác, cập nhật.
            </p>
          </div>

          <div className="bg-cyan-50 dark:bg-cyan-950/20 p-8 rounded-lg">
            <h3 className="text-2xl font-semibold mb-3 text-accent">Cộng Đồng</h3>
            <p className="text-gray-700 dark:text-gray-300">
              Chúng tôi chào mừng cộng đồng du lịch toàn cầu và tận dụng các kinh nghiệm được chia sẻ để giúp người khác.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-ocean-blue text-white py-12 px-4 mt-12">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">Sẵn Sàng Bắt Đầu Hành Trình Của Bạn?</h2>
          <p className="text-lg opacity-90 mb-4">
            Sử dụng chatbot AI của chúng tôi để nhận các gợi ý được cá nhân hóa và bắt đầu lên kế hoạch cho cuộc phiêu lưu tiếp theo của bạn.
          </p>
          <p className="text-sm opacity-75">
            💬 Mở tiện ích trò chuyện ở góc dưới cùng bên phải để bắt đầu!
          </p>
        </div>
      </section>
    </div>
  );
}
