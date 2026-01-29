'use client';

import React from 'react';
import Link from 'next/link';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-dark-gray text-white py-8 mt-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">Du Lịch AI</h3>
            <p className="text-gray-400 text-sm">
              Trợ lý du lịch được hỗ trợ bởi AI cho những chuyến du lịch không thể quên.
            </p>
          </div>

          <div>
            <h4 className="text-md font-semibold mb-4">Khám Phá</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/destinations" className="text-gray-400 hover:text-white transition-colors">
                  Điểm Đến
                </Link>
              </li>
              <li>
                <Link href="/tours" className="text-gray-400 hover:text-white transition-colors">
                  Tour Du Lịch
                </Link>
              </li>
              <li>
                <Link href="/hotels" className="text-gray-400 hover:text-white transition-colors">
                  Khách Sạn
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-md font-semibold mb-4">Khác</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/restaurants" className="text-gray-400 hover:text-white transition-colors">
                  Nhà Hàng
                </Link>
              </li>
              <li>
                <Link href="/about" className="text-gray-400 hover:text-white transition-colors">
                  Về Chúng Tôi
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-md font-semibold mb-4">Liên Hệ</h4>
            <p className="text-gray-400 text-sm">
              Email: hello@dulichai.com
            </p>
          </div>
        </div>

        <div className="border-t border-gray-700 pt-8 flex justify-between items-center">
          <p className="text-gray-400 text-sm">
            © 2024 Du Lịch AI. Bảo lưu mọi quyền.
          </p>
          <div className="flex gap-4">
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              Twitter
            </a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              Facebook
            </a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              Instagram
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};
