'use client';

import React, { useEffect, useState } from 'react';
import { AdminLayout } from '@/components/admin/AdminLayout';
import { DataTable, ColumnDef } from '@/components/admin/DataTable';
import { EntityForm } from '@/components/admin/EntityForm';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { useAdminCRUD } from '@/hooks/useAdminCRUD';
import { Activity } from '@/types';
import { z } from 'zod';

const activitySchema = z.object({
  type: z.string().min(2, 'Loại hoạt động bắt buộc'),
  price: z.coerce.number().min(0, 'Giá phải là số dương'),
  duration: z.string().min(2, 'Thời lượng bắt buộc'),
  description: z.string().min(10, 'Mô tả phải có ít nhất 10 ký tự'),
  destination_id: z.string().optional(),
  image_url: z.string().url('Phải là URL hợp lệ').optional().or(z.literal('')),
});

type ActivityFormData = z.infer<typeof activitySchema>;

const columns: ColumnDef<Activity>[] = [
  { key: 'type', label: 'Loại Hoạt Động' },
  {
    key: 'price',
    label: 'Giá',
    render: (value) => `$${value}`,
  },
  { key: 'duration', label: 'Thời Lượng' },
];

export default function ActivitiesPage() {
  const { data, isLoading, error, fetchData, createItem, updateItem, deleteItem } =
    useAdminCRUD<Activity>({ endpoint: 'activities' });

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<Activity | null>(null);
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

  const handleEdit = (item: Activity) => {
    setEditingItem(item);
    setSubmitError(null);
    setIsDialogOpen(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Bạn có chắc chắn muốn xóa hoạt động này không?')) return;
    setDeletingId(id);
    const success = await deleteItem(id);
    if (!success) {
      setSubmitError('Xóa hoạt động thất bại');
    }
    setDeletingId(null);
  };

  const handleSubmit = async (formData: ActivityFormData) => {
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
      name: 'type',
      label: 'Loại Hoạt Động',
      placeholder: 'ví dụ: Lặn Biển, Leo Núi',
      required: true,
    },
    {
      name: 'price',
      label: 'Giá',
      type: 'number' as const,
      placeholder: '50',
      required: true,
    },
    {
      name: 'duration',
      label: 'Thời Lượng',
      placeholder: 'ví dụ: 2 giờ, Cả ngày',
      required: true,
    },
    {
      name: 'description',
      label: 'Mô Tả',
      type: 'textarea' as const,
      placeholder: 'Mô tả hoạt động này...',
      required: true,
    },
    {
      name: 'destination_id',
      label: 'ID Điểm Đến (tùy chọn)',
      placeholder: 'ID điểm đến',
      required: false,
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
            Quản Lý Hoạt Động
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Tạo, xem, cập nhật và xóa các hoạt động du lịch
          </p>
        </div>

        <DataTable
          title="Danh Sách Hoạt Động"
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

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {editingItem ? 'Chỉnh Sửa Hoạt Động' : 'Thêm Hoạt Động Mới'}
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
            schema={activitySchema}
          />
        </DialogContent>
      </Dialog>
    </AdminLayout>
  );
}