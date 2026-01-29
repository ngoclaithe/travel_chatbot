'use client';

import React, { useEffect, useState } from 'react';
import { AdminLayout } from '@/components/admin/AdminLayout';
import { DataTable, ColumnDef } from '@/components/admin/DataTable';
import { EntityForm } from '@/components/admin/EntityForm';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { useAdminCRUD } from '@/hooks/useAdminCRUD';
import { Review } from '@/types';
import { z } from 'zod';

const reviewSchema = z.object({
  entity_type: z.enum(['destination', 'hotel', 'restaurant', 'tour']),
  entity_id: z.string().min(1, 'Entity ID is required'),
  rating: z.coerce.number().min(0).max(5, 'Rating must be between 0 and 5'),
  comment: z.string().min(5, 'Comment must be at least 5 characters'),
  author: z.string().optional(),
});

type ReviewFormData = z.infer<typeof reviewSchema>;

const columns: ColumnDef<Review>[] = [
  { key: 'entity_type', label: 'Type' },
  { key: 'entity_id', label: 'Entity ID' },
  {
    key: 'rating',
    label: 'Rating',
    render: (value) => `${value}/5`,
  },
  {
    key: 'comment',
    label: 'Comment',
    render: (value) => String(value).substring(0, 50) + '...',
  },
  { key: 'author', label: 'Author' },
];

export default function ReviewsPage() {
  const { data, isLoading, error, fetchData, createItem, updateItem, deleteItem } =
    useAdminCRUD<Review>({ endpoint: 'reviews' });

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<Review | null>(null);
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

  const handleEdit = (item: Review) => {
    setEditingItem(item);
    setSubmitError(null);
    setIsDialogOpen(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure?')) return;
    setDeletingId(id);
    const success = await deleteItem(id);
    if (!success) {
      setSubmitError('Failed to delete');
    }
    setDeletingId(null);
  };

  const handleSubmit = async (formData: ReviewFormData) => {
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
      name: 'entity_type',
      label: 'Entity Type',
      type: 'select' as const,
      options: [
        { value: 'destination', label: 'Destination' },
        { value: 'hotel', label: 'Hotel' },
        { value: 'restaurant', label: 'Restaurant' },
        { value: 'tour', label: 'Tour' },
      ],
      required: true,
    },
    {
      name: 'entity_id',
      label: 'Entity ID',
      placeholder: 'ID of the entity being reviewed',
      required: true,
    },
    {
      name: 'rating',
      label: 'Rating (0-5)',
      type: 'number' as const,
      placeholder: '4',
      required: true,
    },
    {
      name: 'comment',
      label: 'Review Comment',
      type: 'textarea' as const,
      placeholder: 'Write your review...',
      required: true,
    },
    {
      name: 'author',
      label: 'Author Name (optional)',
      placeholder: 'Anonymous',
      required: false,
    },
  ];

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Manage Reviews
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Create, read, update, and delete reviews
          </p>
        </div>

        <DataTable
          title="Reviews"
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
              {editingItem ? 'Edit Review' : 'Add New Review'}
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
            schema={reviewSchema}
          />
        </DialogContent>
      </Dialog>
    </AdminLayout>
  );
}
