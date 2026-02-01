'use client';

import React, { useEffect, useState } from 'react';
import { AdminLayout } from '@/components/admin/AdminLayout';
import { DataTable, ColumnDef } from '@/components/admin/DataTable';
import { EntityForm } from '@/components/admin/EntityForm';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { useAdminCRUD } from '@/hooks/useAdminCRUD';
import { Transportation } from '@/types';
import { z } from 'zod';

const transportationSchema = z.object({
  from_destination: z.string().min(1, 'Điểm đi là bắt buộc'),
  to_destination: z.string().min(1, 'Điểm đến là bắt buộc'),
  type: z.string().min(2, 'Loại phương tiện là bắt buộc'),
  duration: z.string().min(2, 'Thời gian là bắt buộc'),
  price_range: z.string().min(1, 'Khoảng giá là bắt buộc'),
});

type TransportationFormData = z.infer<typeof transportationSchema>;

const columns: ColumnDef<Transportation>[] = [
  { key: 'from_destination', label: 'Từ' },
  { key: 'to_destination', label: 'Đến' },
  { key: 'type', label: 'Loại' },
  { key: 'duration', label: 'Thời Gian' },
  { key: 'price_range', label: 'Khoảng Giá' },
];

export default function TransportationPage() {
  const { data, isLoading, error, fetchData, createItem, updateItem, deleteItem } =
    useAdminCRUD<Transportation>({ endpoint: 'transportation' });

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<Transportation | null>(null);
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

  const handleEdit = (item: Transportation) => {
    setEditingItem(item);
    setSubmitError(null);
    setIsDialogOpen(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Bạn có chắc chắn muốn xóa không?')) return;
    setDeletingId(id);
    const success = await deleteItem(id);
    if (!success) {
      setSubmitError('Xóa thất bại');
    }
    setDeletingId(null);
  };

  const handleSubmit = async (formData: TransportationFormData) => {
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
      name: 'from_destination',
      label: 'Điểm Đi',
      placeholder: 'ví dụ: Bangkok',
      required: true,
    },
    {
      name: 'to_destination',
      label: 'Điểm Đến',
      placeholder: 'ví dụ: Phuket',
      required: true,
    },
    {
      name: 'type',
      label: 'Loại Phương Tiện',
      placeholder: 'ví dụ: Máy bay, Xe buýt',
      required: true,
    },
    {
      name: 'duration',
      label: 'Thời Gian',
      placeholder: 'ví dụ: 2 giờ',
      required: true,
    },
    {
      name: 'price_range',
      label: 'Khoảng Giá',
      placeholder: '$$',
      required: true,
    },
  ];

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Quản Lý Vận Chuyển
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Các lựa chọn vận chuyển giữa các điểm đến
          </p>
        </div>

        <DataTable
          title="Các Tuyến Vận Chuyển"
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
              {editingItem ? 'Chỉnh Sửa Tuyến' : 'Thêm Tuyến Vận Chuyển'}
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
            schema={transportationSchema}
          />
        </DialogContent>
      </Dialog>
    </AdminLayout>
  );
}
