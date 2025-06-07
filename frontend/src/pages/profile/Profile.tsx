
import { useAuth } from "@/hooks/useAuth";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Edit, Mail, Phone, MapPin, Calendar, GraduationCap } from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Link } from "react-router-dom";

const Profile = () => {
  const { user } = useAuth();

  // Mock user data - in real app this would come from API
  const profileData = {
    ...user,
    phone: "+1 (555) 123-4567",
    address: "123 Education Ave, Learning City, LC 12345",
    dateJoined: "September 2023",
    department: user?.role === 'student' ? 'Computer Science' : 'Mathematics',
    studentId: user?.role === 'student' ? 'STU-2024-001' : undefined,
    employeeId: user?.role !== 'student' ? 'EMP-2023-156' : undefined,
    gpa: user?.role === 'student' ? '3.75' : undefined,
    courses: user?.role === 'student' ? 4 : undefined,
    subjects: user?.role === 'teacher' ? ['Calculus I', 'Statistics', 'Linear Algebra'] : undefined,
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Profile Header */}
        <Card className="border-0 shadow-md">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
              <Avatar className="h-24 w-24">
                <AvatarImage src={user?.avatar} />
                <AvatarFallback className="text-2xl">
                  {user?.firstName?.[0]}{user?.lastName?.[0]}
                </AvatarFallback>
              </Avatar>
              
              <div className="flex-1 space-y-2">
                <div className="flex flex-col md:flex-row md:items-center gap-4">
                  <h1 className="text-3xl font-bold text-gray-900">
                    {profileData.firstName} {profileData.lastName}
                  </h1>
                  <Badge variant="secondary" className="w-fit capitalize">
                    {profileData.role}
                  </Badge>
                </div>
                
                <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                  <div className="flex items-center gap-1">
                    <Mail className="h-4 w-4" />
                    {profileData.email}
                  </div>
                  <div className="flex items-center gap-1">
                    <Phone className="h-4 w-4" />
                    {profileData.phone}
                  </div>
                  <div className="flex items-center gap-1">
                    <Calendar className="h-4 w-4" />
                    Joined {profileData.dateJoined}
                  </div>
                </div>
              </div>
              
              <Link to="/profile/edit">
                <Button className="flex items-center gap-2">
                  <Edit className="h-4 w-4" />
                  Edit Profile
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Personal Information */}
          <Card className="lg:col-span-2 border-0 shadow-md">
            <CardHeader>
              <CardTitle>Personal Information</CardTitle>
              <CardDescription>Your basic profile information</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="text-sm font-medium text-gray-600">First Name</label>
                  <p className="text-gray-900 font-medium">{profileData.firstName}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">Last Name</label>
                  <p className="text-gray-900 font-medium">{profileData.lastName}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">Email Address</label>
                  <p className="text-gray-900 font-medium">{profileData.email}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">Phone Number</label>
                  <p className="text-gray-900 font-medium">{profileData.phone}</p>
                </div>
                <div className="md:col-span-2">
                  <label className="text-sm font-medium text-gray-600">Address</label>
                  <p className="text-gray-900 font-medium flex items-center gap-2">
                    <MapPin className="h-4 w-4 text-gray-500" />
                    {profileData.address}
                  </p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">Department</label>
                  <p className="text-gray-900 font-medium">{profileData.department}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">
                    {profileData.role === 'student' ? 'Student ID' : 'Employee ID'}
                  </label>
                  <p className="text-gray-900 font-medium">
                    {profileData.studentId || profileData.employeeId}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Quick Stats */}
          <Card className="border-0 shadow-md">
            <CardHeader>
              <CardTitle>Quick Stats</CardTitle>
              <CardDescription>Your key metrics</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {profileData.role === 'student' && (
                <>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Current GPA</span>
                    <span className="font-semibold text-lg text-green-600">{profileData.gpa}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Enrolled Courses</span>
                    <span className="font-semibold text-lg">{profileData.courses}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Attendance Rate</span>
                    <span className="font-semibold text-lg text-blue-600">94%</span>
                  </div>
                </>
              )}
              
              {profileData.role === 'teacher' && (
                <>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Subjects Teaching</span>
                    <span className="font-semibold text-lg">{profileData.subjects?.length}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Total Students</span>
                    <span className="font-semibold text-lg">85</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Rating</span>
                    <span className="font-semibold text-lg text-yellow-600">4.8/5</span>
                  </div>
                </>
              )}
              
              {(profileData.role === 'admin' || profileData.role === 'staff') && (
                <>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Years of Service</span>
                    <span className="font-semibold text-lg">3</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Department</span>
                    <span className="font-semibold text-sm">{profileData.department}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Performance</span>
                    <span className="font-semibold text-lg text-green-600">Excellent</span>
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Additional Information */}
        {profileData.role === 'teacher' && profileData.subjects && (
          <Card className="border-0 shadow-md">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <GraduationCap className="h-5 w-5" />
                Subjects Teaching
              </CardTitle>
              <CardDescription>Current teaching assignments</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {profileData.subjects.map((subject, index) => (
                  <Badge key={index} variant="outline" className="px-3 py-1">
                    {subject}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Account Settings */}
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle>Account Settings</CardTitle>
            <CardDescription>Manage your account preferences</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium">Email Notifications</h4>
                  <p className="text-sm text-gray-600">Receive updates via email</p>
                </div>
                <Button variant="outline" size="sm">Configure</Button>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium">Privacy Settings</h4>
                  <p className="text-sm text-gray-600">Control who can see your information</p>
                </div>
                <Button variant="outline" size="sm">Manage</Button>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium">Security</h4>
                  <p className="text-sm text-gray-600">Password and two-factor authentication</p>
                </div>
                <Button variant="outline" size="sm">Update</Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default Profile;
