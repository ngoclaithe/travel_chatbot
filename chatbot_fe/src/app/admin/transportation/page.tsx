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
  from_destination: z.string().min(1, 'From destination is required'),
  to_destination: z.string().min(1, 'To destination is required'),
  type: z.string().min(2, 'Transport type is required'),
  duration: z.string().min(2, 'Duration is required'),
  price_range: z.string().min(1, 'Price range is required'),
});

type TransportationFormData = z.infer<typeof transportationSchema>;

const columns: ColumnDef<Transportation>[] = [
  { key: 'from_destination', label: 'From' },
  { key: 'to_destination', label: 'To' },
  { key: 'type', label: 'Type' },
  { key: 'duration', label: 'Duration' },
  { key: 'price_range', label: 'Price Range' },
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
    if (!confirm('Are you sure?')) return;
    setDeletingId(id);
    const success = await deleteItem(id);
    if (!success) {
      setSubmitError('Failed to delete');
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
      setSubmitError(err instanceof Error ? err.message : 'Failed to save');
    } finally {
      setIsSubmitting(false);
    }
  };

  const formFields = [
    {
      name: 'from_destination',
      label: 'From Destination',
      placeholder: 'e.g., Bangkok',
      required: true,
    },
    {
      name: 'to_destination',
      label: 'To Destination',
      placeholder: 'e.g., Phuket',
      required: true,
    },
    {
      name: 'type',
      label: 'Transport Type',
      placeholder: 'e.g., Flight, Bus, Train',
      required: true,
    },
    {
      name: 'duration',
      label: 'Duration',
      placeholder: 'e.g., 2 hours',
      required: true,
    },
    {
      name: 'price_range',
      label: 'Price Range',
      placeholder: '$$',
      required: true,
    },
  ];

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Manage Transportation
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Transportation options between destinations
          </p>
        </div>

        <DataTable
          title="Transportation Routes"
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
              {editingItem ? 'Edit Route' : 'Add Transportation Route'}
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
