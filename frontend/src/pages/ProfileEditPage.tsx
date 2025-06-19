import React, { useState, useEffect, useCallback } from 'react'; // Added useCallback
import { useAuth } from '@/contexts/useAuth'; // Corrected import path
import { authAPI } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
import { UserProfileData, User } from '@/contexts/AuthContextTypes'; // Added User

const ProfilePage = () => {
  const { user, refreshUserData } = useAuth(); // Changed setUser to refreshUserData
  
  // Initialize formData with fields from User and UserProfileData
  const [formData, setFormData] = useState<Partial<User & UserProfileData>>({
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '', // from UserProfileData
    // Add other fields from UserProfileData if they are editable here
    // e.g., student_id, teacher_id, etc. if applicable and part of UserProfileData
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (user) {
      setFormData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || '',
        phone_number: user.profile_data?.phone_number || user.phone_number || '', // Check both profile_data and user
        // Populate other fields from user or user.profile_data as needed
      });
    }
  }, [user]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user?.id) {
      toast.error('User not found. Cannot update profile.');
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      // Prepare data for API: only send fields that are part of UserProfileUpdateData
      // UserProfileUpdateData defines what authAPI.updateProfile expects.
      const updateData: { 
        first_name?: string; 
        last_name?: string; 
        email?: string; 
        phone_number?: string; 
        // Add other updatable fields here if they are part of the backend serializer for user update
      } = {};

      if (formData.first_name !== undefined) updateData.first_name = formData.first_name;
      if (formData.last_name !== undefined) updateData.last_name = formData.last_name;
      if (formData.email !== undefined) updateData.email = formData.email;
      // Assuming phone_number is part of the user update on the backend.
      // If it's part of a separate profile model, it might need a different API call.
      if (formData.phone_number !== undefined) updateData.phone_number = formData.phone_number;

      // Ensure user.id is a string, as expected by authAPI.updateProfile
      await authAPI.updateProfile(user.id, updateData);
      
      await refreshUserData(); // Refresh user data from context
      toast.success('Profile updated successfully!');
    } catch (err: unknown) { // Changed any to unknown
      console.error('Failed to update profile:', err);
      const typedError = err as { response?: { data?: { detail?: string } }, message?: string };
      const errorMessage = typedError.response?.data?.detail || typedError.message || 'Failed to update profile.';
      setError(errorMessage);
      toast.error(errorMessage + ' Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  if (!user) {
    return (
        <div className="p-6">Loading profile...</div>
    );
  }

  return (
      <div className="p-6">
        <Card className="max-w-2xl mx-auto">
          <CardHeader>
            <CardTitle>My Profile</CardTitle>
            <CardDescription>Update your personal information.</CardDescription>
          </CardHeader>
          <CardContent>
            {error && <p className="text-red-500 mb-4">{error}</p>}
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="first_name">First Name</Label>
                  <Input
                    id="first_name"
                    value={formData.first_name || ''}
                    onChange={handleChange}
                    disabled={isLoading}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="last_name">Last Name</Label>
                  <Input
                    id="last_name"
                    value={formData.last_name || ''}
                    onChange={handleChange}
                    disabled={isLoading}
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email || ''}
                  onChange={handleChange}
                  disabled={isLoading}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="phone_number">Phone Number</Label>
                <Input
                  id="phone_number"
                  value={formData.phone_number || ''}
                  onChange={handleChange}
                  disabled={isLoading}
                />
              </div>
              {/* Add more fields as necessary, e.g., for password change */}
              <Button type="submit" disabled={isLoading} className="w-full">
                {isLoading ? 'Saving...' : 'Save Changes'}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
  );
};

export default ProfilePage;
