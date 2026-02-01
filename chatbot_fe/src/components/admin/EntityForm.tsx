'use client';

import React, { useState } from 'react';
import { useForm, FieldValues } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { AlertCircle, Loader2 } from 'lucide-react';
import axiosClient from '@/lib/axiosClient';

interface FormField {
  name: string;
  label: string;
  type?: 'text' | 'email' | 'number' | 'textarea' | 'select' | 'checkbox' | 'image';
  placeholder?: string;
  required?: boolean;
  options?: { value: string; label: string }[];
}

export interface EntityFormProps<T extends z.ZodTypeAny> {
  title: string;
  fields: FormField[];
  defaultValues?: Partial<z.infer<T>>;
  onSubmit: (data: z.infer<T>) => Promise<void>;
  isLoading?: boolean;
  error?: string | null;
  onCancel?: () => void;
  schema: T;
}

export function EntityForm<T extends z.ZodTypeAny>({
  title,
  fields,
  defaultValues,
  onSubmit,
  isLoading = false,
  error = null,
  onCancel,
  schema,
}: EntityFormProps<T>) {
  type FormData = z.infer<T> & FieldValues;

  const { register, handleSubmit, formState: { errors }, setValue, watch } = useForm<FormData>({
    resolver: zodResolver(schema as any),
    defaultValues: defaultValues as any,
  });

  const [uploadLoading, setUploadLoading] = useState(false);

  const handleImageUpload = async (file: File, fieldName: string) => {
    try {
      setUploadLoading(true);
      const formData = new FormData();
      formData.append('file', file);

      const response = await axiosClient.post('/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setValue(fieldName as any, response.data.url, { shouldValidate: true, shouldDirty: true });
    } catch (error) {
      console.error("Upload failed", error);
    } finally {
      setUploadLoading(false);
    }
  };

  const onSubmitHandler = async (data: FormData) => {
    await onSubmit(data as z.infer<T>);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent className="max-h-[70vh] overflow-y-auto">
        <form onSubmit={handleSubmit(onSubmitHandler)} className="space-y-6">
          {error && (
            <div className="bg-destructive/10 border border-destructive text-destructive p-4 rounded-lg flex items-center gap-3">
              <AlertCircle className="w-5 h-5 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {fields.map((field) => (
            <div key={field.name} className="space-y-2">
              <Label htmlFor={field.name}>
                {field.label}
                {field.required && <span className="text-destructive ml-1">*</span>}
              </Label>

              {field.type === 'textarea' ? (
                <textarea
                  id={field.name}
                  placeholder={field.placeholder}
                  disabled={isLoading}
                  className="flex min-h-24 w-full rounded-md border border-input bg-background px-3 py-2 text-base shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                  {...register(field.name as any)}
                />
              ) : field.type === 'select' ? (
                <select
                  id={field.name}
                  disabled={isLoading}
                  className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-base shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                  {...register(field.name as any)}
                >
                  <option value="">Select {field.label}</option>
                  {field.options?.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              ) : field.type === 'image' ? (
                <div className="space-y-4">
                  {watch(field.name as any) && (
                    <div className="relative w-32 h-32 rounded-lg overflow-hidden border">
                      <img
                        src={watch(field.name as any)}
                        alt="Preview"
                        className="w-full h-full object-cover"
                      />
                    </div>
                  )}
                  <Input
                    id={field.name}
                    type="file"
                    accept="image/*"
                    disabled={isLoading || uploadLoading}
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      if (file) handleImageUpload(file, field.name);
                    }}
                  />
                </div>
              ) : field.type === 'checkbox' ? (
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    id={field.name}
                    type="checkbox"
                    disabled={isLoading}
                    className="w-4 h-4 rounded border border-input bg-background cursor-pointer disabled:cursor-not-allowed disabled:opacity-50"
                    {...register(field.name as any)}
                  />
                  <span className="text-sm text-muted-foreground">Mark as best time</span>
                </label>
              ) : (
                <Input
                  id={field.name}
                  type={field.type || 'text'}
                  step={field.type === 'number' ? '0.1' : undefined}
                  placeholder={field.placeholder}
                  disabled={isLoading}
                  {...register(field.name as any)}
                />
              )}

              {field.name in errors && (
                <p className="text-sm text-destructive">
                  {(errors[field.name as keyof typeof errors] as any)?.message}
                </p>
              )}
            </div>
          ))}

          <div className="flex gap-4 pt-4">
            <Button
              type="submit"
              className="bg-ocean-blue hover:bg-ocean-dark flex-1"
              disabled={isLoading || uploadLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Saving...
                </>
              ) : (
                'Save'
              )}
            </Button>
            {onCancel && (
              <Button
                type="button"
                variant="outline"
                onClick={onCancel}
                disabled={isLoading}
              >
                Cancel
              </Button>
            )}
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
