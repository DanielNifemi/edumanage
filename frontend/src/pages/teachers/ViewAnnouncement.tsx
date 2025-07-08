import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast";
import { ArrowLeft, Edit, Share, Eye, Calendar } from "lucide-react";

interface Announcement {
  id: number;
  title: string;
  content: string;
  priority: 'low' | 'normal' | 'high' | 'urgent';
  target_audience: 'all' | 'students' | 'teachers' | 'staff';
  is_published: boolean;
  created_at: string;
  updated_at: string;
  author_name?: string;
  views_count?: number;
}

const ViewAnnouncement = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const [announcement, setAnnouncement] = useState<Announcement | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadAnnouncement = async () => {
      try {
        setLoading(true);
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Mock data - replace with actual API call
        const mockAnnouncement: Announcement = {
          id: parseInt(id || '1'),
          title: "Mid-term Exam Schedule",
          content: `The mid-term examinations will be conducted from March 15-22, 2025. Please ensure all students are prepared and have their admit cards ready.

Schedule:
- Monday, March 15: Mathematics (9:00 AM - 11:00 AM)
- Tuesday, March 16: English (9:00 AM - 11:00 AM)
- Wednesday, March 17: Science (9:00 AM - 11:00 AM)
- Thursday, March 18: Social Studies (9:00 AM - 11:00 AM)
- Friday, March 19: Computer Science (9:00 AM - 11:00 AM)

Important Notes:
1. Students must arrive 30 minutes before the exam
2. Bring valid ID and admit card
3. No electronic devices allowed
4. Contact the examination office for any queries

Good luck to all students!`,
          priority: 'high',
          target_audience: 'students',
          is_published: true,
          created_at: '2025-03-01T10:00:00Z',
          updated_at: '2025-03-01T10:00:00Z',
          author_name: 'John Doe',
          views_count: 156
        };
        
        setAnnouncement(mockAnnouncement);
      } catch (error) {
        console.error('Error loading announcement:', error);
        toast({
          title: "Error",
          description: "Failed to load announcement.",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
      }
    };

    loadAnnouncement();
  }, [id, toast]);

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'bg-red-100 text-red-800';
      case 'high': return 'bg-orange-100 text-orange-800';
      case 'normal': return 'bg-blue-100 text-blue-800';
      case 'low': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (isPublished: boolean) => {
    return isPublished ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800';
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="p-6">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-gray-200 rounded w-1/4"></div>
            <div className="h-64 bg-gray-200 rounded"></div>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  if (!announcement) {
    return (
      <DashboardLayout>
        <div className="p-6">
          <Card>
            <CardContent className="p-12 text-center">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Announcement not found</h3>
              <p className="text-gray-600 mb-4">The announcement you're looking for doesn't exist.</p>
              <Button onClick={() => navigate('/teacher/announcements')}>
                Back to Announcements
              </Button>
            </CardContent>
          </Card>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="p-6 max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate('/teacher/announcements')}
              className="flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Announcements
            </Button>
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigate(`/teacher/announcements/${announcement.id}/edit`)}
              className="flex items-center gap-2"
            >
              <Edit className="h-4 w-4" />
              Edit
            </Button>
            <Button
              variant="outline"
              size="sm"
              className="flex items-center gap-2"
            >
              <Share className="h-4 w-4" />
              Share
            </Button>
          </div>
        </div>

        {/* Announcement Content */}
        <Card>
          <CardHeader>
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <CardTitle className="text-2xl">{announcement.title}</CardTitle>
                  <Badge className={getPriorityColor(announcement.priority)}>
                    {announcement.priority.charAt(0).toUpperCase() + announcement.priority.slice(1)}
                  </Badge>
                  <Badge className={getStatusColor(announcement.is_published)}>
                    {announcement.is_published ? 'Published' : 'Draft'}
                  </Badge>
                </div>
                
                <div className="flex items-center gap-4 text-sm text-gray-600">
                  <div className="flex items-center gap-1">
                    <Calendar className="h-4 w-4" />
                    <span>Created: {new Date(announcement.created_at).toLocaleDateString()}</span>
                  </div>
                  <span>•</span>
                  <span>Target: {announcement.target_audience}</span>
                  <span>•</span>
                  <span>Author: {announcement.author_name}</span>
                  {announcement.is_published && (
                    <>
                      <span>•</span>
                      <div className="flex items-center gap-1">
                        <Eye className="h-4 w-4" />
                        <span>{announcement.views_count} views</span>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="prose max-w-none">
              <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                {announcement.content}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="mt-6 flex gap-3">
          <Button
            onClick={() => navigate(`/teacher/announcements/${announcement.id}/edit`)}
            className="flex items-center gap-2"
          >
            <Edit className="h-4 w-4" />
            Edit Announcement
          </Button>
          <Button
            variant="outline"
            className="flex items-center gap-2"
          >
            <Share className="h-4 w-4" />
            Share
          </Button>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default ViewAnnouncement;
