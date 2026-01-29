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
  type: z.string().min(2, 'Type is required'),
  price: z.coerce.number().min(0, 'Price must be positive'),
  duration: z.string().min(2, 'Duration is required'),
  description: z.string().min(10, 'Description must be at least 10 characters'),
  destination_id: z.string().optional(),
  image_url: z.string().url('Must be a valid URL').optional().or(z.literal('')),
});

type ActivityFormData = z.infer<typeof activitySchema>;

const columns: ColumnDef<Activity>[] = [
  { key: 'type', label: 'Activity Type' },
  {
    key: 'price',
    label: 'Price',
    render: (value) => `$${value}`,
  },
  { key: 'duration', label: 'Duration' },
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
    if (!confirm('Are you sure you want to delete this activity?')) return;
    setDeletingId(id);
    const success = await deleteItem(id);
    if (!success) {
      setSubmitError('Failed to delete activity');
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
      setSubmitError(err instanceof Error ? err.message : 'Failed to save');
    } finally {
      setIsSubmitting(false);
    }
  };

  const formFields = [
    {
      name: 'type',
      label: 'Activity Type',
      placeholder: 'e.g., Scuba Diving, Hiking',
      required: true,
    },
    {
      name: 'price',
      label: 'Price',
      type: 'number' as const,
      placeholder: '50',
      required: true,
    },
    {
      name: 'duration',
      label: 'Duration',
      placeholder: 'e.g., 2 hours, Full day',
      required: true,
    },
    {
      name: 'description',
      label: 'Description',
      type: 'textarea' as const,
      placeholder: 'Describe this activity...',
      required: true,
    },
    {
      name: 'destination_id',
      label: 'Destination ID (optional)',
      placeholder: 'Activity destination ID',
      required: false,
    },
    {
      name: 'image_url',
      label: 'Image URL',
      placeholder: 'https://...',
      required: false,
    },
  ];

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Manage Activities
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Create, read, update, and delete travel activities
          </p>
        </div>

        <DataTable
          title="Activities"
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
              {editingItem ? 'Edit Activity' : 'Add New Activity'}
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