'use client';

import React, { useEffect, useState } from 'react';
import { AdminLayout } from '@/components/admin/AdminLayout';
import { DataTable, ColumnDef } from '@/components/admin/DataTable';
import { EntityForm } from '@/components/admin/EntityForm';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { useAdminCRUD } from '@/hooks/useAdminCRUD';
import { Restaurant } from '@/types';
import { z } from 'zod';

const restaurantSchema = z.object({
  name: z.string().min(2, 'Tên phải có ít nhất 2 ký tự'),
  destination_id: z.string().min(1, 'Điểm đến là bắt buộc'),
  cuisine_type: z.string().min(2, 'Loại ẩm thực là bắt buộc'),
  price_range: z.string().min(1, 'Khoảng giá là bắt buộc'),
  rating: z.coerce.number().min(0).max(5, 'Đánh giá phải từ 0 đến 5'),
  image_url: z.string().url('Phải là URL hợp lệ').optional().or(z.literal('')),
});

type RestaurantFormData = z.infer<typeof restaurantSchema>;

const columns: ColumnDef<Restaurant>[] = [
  { key: 'name', label: 'Tên Nhà Hàng' },
  {
    key: 'image_url',
    label: 'Hình Ảnh',
    render: (value) => value ? <img src={value as string} alt="Restaurant" className="w-16 h-10 object-cover rounded" /> : null
  },
  { key: 'destination_id', label: 'Điểm Đến' },
  { key: 'cuisine_type', label: 'Loại Ẩm Thực' },
  { key: 'price_range', label: 'Khoảng Giá' },
  {
    key: 'rating',
    label: 'Đánh Giá',
    render: (value) => `${value}/5`,
  },
];

export default function RestaurantsPage() {
  const { data, isLoading, error, fetchData, createItem, updateItem, deleteItem } =
    useAdminCRUD<Restaurant>({ endpoint: 'restaurants' });

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<Restaurant | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleAdd = () => {
    setEditingItem(null);
    setSubmitError(null);
    setIsDialogOpen(true);
  };

  const handleEdit = (item: Restaurant) => {
    setEditingItem(item);
    setSubmitError(null);
    setIsDialogOpen(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Bạn có chắc chắn muốn xóa nhà hàng này không?')) return;
    setDeletingId(id);
    const success = await deleteItem(id);
    if (!success) {
      setSubmitError('Xóa nhà hàng thất bại');
    }
    setDeletingId(null);
  };

  const handleSubmit = async (formData: RestaurantFormData) => {
    try {
      setIsSubmitting(true);
      setSubmitError(null);

      if (editingItem) {
        await updateItem(editingItem.id, formData);
      } else {
        await createItem(formData);
      }

      setIsDialogOpen(false);
      setEditingItem(null);
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : 'Lưu thất bại');
    } finally {
      setIsSubmitting(false);
    }
  };

  const formFields = [
    {
      name: 'name',
      label: 'Tên Nhà Hàng',
      placeholder: 'ví dụ: La Belle Vie',
      required: true,
    },
    {
      name: 'destination_id',
      label: 'ID Điểm Đến',
      placeholder: 'ID điểm đến của nhà hàng',
      required: true,
    },
    {
      name: 'cuisine_type',
      label: 'Loại Ẩm Thực',
      placeholder: 'ví dụ: Pháp, Ý, Thái',
      required: true,
    },
    {
      name: 'price_range',
      label: 'Khoảng Giá',
      placeholder: '$$',
      required: true,
    },
    {
      name: 'rating',
      label: 'Đánh Giá (0-5)',
      type: 'number' as const,
      placeholder: '4.5',
      required: true,
    },
    {
      name: 'image_url',
      label: 'Hình Ảnh',
      type: 'image' as const,
      required: false,
    },
  ];

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Quản Lý Nhà Hàng
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Tạo, xem, cập nhật và xóa các nhà hàng
          </p>
        </div>

        <DataTable
          title="Danh Sách Nhà Hàng"
          columns={columns}
          data={data}
          isLoading={isLoading}
          error={error}
          onAdd={handleAdd}
          onEdit={handleEdit}
          onDelete={handleDelete}
          isDeleting={deletingId}
        />
      </div>

      {/* Form Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] flex flex-col">
          <DialogHeader>
            <DialogTitle>
              {editingItem ? 'Chỉnh Sửa Nhà Hàng' : 'Thêm Nhà Hàng Mới'}
            </DialogTitle>
          </DialogHeader>

          <EntityForm
            title=""
            fields={formFields}
            defaultValues={editingItem || undefined}
            onSubmit={handleSubmit}
            isLoading={isSubmitting}
            error={submitError}
            onCancel={() => setIsDialogOpen(false)}
            schema={restaurantSchema}
          />
        </DialogContent>
      </Dialog>
    </AdminLayout>
  );
}
