
import React from 'react';
import { useAuth } from '@/contexts/useAuth';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';

const ProfilePage = () => {
  const { user } = useAuth();

  if (!user) {
    return <div className="p-6">Loading profile...</div>;
  }

  return (
    <div className="p-6">
      <Card className="max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle>My Profile</CardTitle>
          <CardDescription>View your personal information.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <p className="font-semibold">First Name:</p>
            <p>{user.first_name}</p>
          </div>
          <div>
            <p className="font-semibold">Last Name:</p>
            <p>{user.last_name}</p>
          </div>
          <div>
            <p className="font-semibold">Email:</p>
            <p>{user.email}</p>
          </div>
          <div>
            <p className="font-semibold">Phone Number:</p>
            <p>{user.profile_data?.phone_number || user.phone_number || 'Not provided'}</p>
          </div>
          <Link to="/profile/edit">
            <Button>Edit Profile</Button>
          </Link>
        </CardContent>
      </Card>
    </div>
  );
};

export default ProfilePage;
