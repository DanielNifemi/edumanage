import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { useToast } from "@/hooks/use-toast";
import { ArrowLeft, Save, Send, AlertTriangle } from "lucide-react";

interface AnnouncementFormData {
  title: string;
  content: string;
  priority: 'low' | 'normal' | 'high' | 'urgent';
  target_audience: 'all' | 'students' | 'teachers' | 'staff';
  is_published: boolean;
}

const CreateAnnouncement = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { toast } = useToast();
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(!!id);
  const isEditMode = !!id;
  
  const [formData, setFormData] = useState<AnnouncementFormData>({
    title: '',
    content: '',
    priority: 'normal',
    target_audience: 'all',
    is_published: false
  });

  // Load existing announcement data if in edit mode
  useEffect(() => {
    if (isEditMode) {
      const loadAnnouncement = async () => {
        try {
          setInitialLoading(true);
          
          // Simulate API call
          await new Promise(resolve => setTimeout(resolve, 500));
          
          // Mock data - replace with actual API call
          const mockAnnouncement = {
            id: parseInt(id!),
            title: "Mid-term Exam Schedule",
            content: "The mid-term examinations will be conducted from March 15-22, 2025. Please ensure all students are prepared and have their admit cards ready.",
            priority: 'high' as const,
            target_audience: 'students' as const,
            is_published: true
          };
          
          setFormData(mockAnnouncement);
        } catch (error) {
          console.error('Error loading announcement:', error);
          toast({
            title: "Error",
            description: "Failed to load announcement.",
            variant: "destructive",
          });
        } finally {
          setInitialLoading(false);
        }
      };

      loadAnnouncement();
    }
  }, [id, isEditMode, toast]);

  const handleSubmit = async (publish: boolean = false) => {
    try {
      if (!formData.title.trim() || !formData.content.trim()) {
        toast({
          title: "Error",
          description: "Please fill in all required fields.",
          variant: "destructive",
        });
        return;
      }

      setLoading(true);
      
      // TODO: Replace with actual API call
      const announcementData = {
        ...formData,
        is_published: publish,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };

      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));

      toast({
        title: "Success",
        description: `Announcement ${isEditMode ? 'updated' : 'created'} ${publish ? 'and published' : 'as draft'} successfully.`,
      });

      // Navigate back to announcements list
      navigate('/teacher/announcements');
    } catch (error) {
      console.error('Error saving announcement:', error);
      toast({
        title: "Error",
        description: `Failed to ${isEditMode ? 'update' : 'create'} announcement. Please try again.`,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSaveDraft = () => handleSubmit(false);
  const handlePublish = () => handleSubmit(true);

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'text-red-600';
      case 'high': return 'text-orange-600';
      case 'normal': return 'text-blue-600';
      case 'low': return 'text-gray-600';
      default: return 'text-gray-600';
    }
  };

  if (initialLoading) {
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

  return (
    <DashboardLayout>
      <div className="p-6 max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-4 mb-6">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate('/teacher/announcements')}
            className="flex items-center gap-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Announcements
          </Button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              {isEditMode ? 'Edit Announcement' : 'Create New Announcement'}
            </h1>
            <p className="text-gray-600 mt-1">
              {isEditMode 
                ? 'Update your announcement details' 
                : 'Share important information with your students and colleagues'
              }
            </p>
          </div>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>{isEditMode ? 'Edit Announcement' : 'Announcement Details'}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Title */}
            <div>
              <Label htmlFor="title">Title *</Label>
              <Input
                id="title"
                value={formData.title}
                onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                placeholder="Enter announcement title..."
                className="mt-1"
                required
              />
            </div>

            {/* Content */}
            <div>
              <Label htmlFor="content">Content *</Label>
              <Textarea
                id="content"
                value={formData.content}
                onChange={(e) => setFormData(prev => ({ ...prev, content: e.target.value }))}
                placeholder="Write your announcement content here..."
                className="mt-1 min-h-[200px]"
                required
              />
            </div>

            {/* Priority and Target Audience */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="priority">Priority</Label>
                <Select 
                  value={formData.priority} 
                  onValueChange={(value: 'low' | 'normal' | 'high' | 'urgent') => 
                    setFormData(prev => ({ ...prev, priority: value }))
                  }
                >
                  <SelectTrigger className="mt-1">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="low">
                      <span className="flex items-center gap-2">
                        <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
                        Low
                      </span>
                    </SelectItem>
                    <SelectItem value="normal">
                      <span className="flex items-center gap-2">
                        <span className="w-2 h-2 bg-blue-400 rounded-full"></span>
                        Normal
                      </span>
                    </SelectItem>
                    <SelectItem value="high">
                      <span className="flex items-center gap-2">
                        <span className="w-2 h-2 bg-orange-400 rounded-full"></span>
                        High
                      </span>
                    </SelectItem>
                    <SelectItem value="urgent">
                      <span className="flex items-center gap-2">
                        <span className="w-2 h-2 bg-red-400 rounded-full"></span>
                        Urgent
                      </span>
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="target_audience">Target Audience</Label>
                <Select 
                  value={formData.target_audience} 
                  onValueChange={(value: 'all' | 'students' | 'teachers' | 'staff') => 
                    setFormData(prev => ({ ...prev, target_audience: value }))
                  }
                >
                  <SelectTrigger className="mt-1">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Users</SelectItem>
                    <SelectItem value="students">Students Only</SelectItem>
                    <SelectItem value="teachers">Teachers Only</SelectItem>
                    <SelectItem value="staff">Staff Only</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Preview */}
            <div>
              <Label>Preview</Label>
              <div className="mt-2 p-4 border rounded-lg bg-gray-50">
                <div className="flex items-center gap-2 mb-2">
                  <h3 className="font-semibold text-lg">{formData.title || 'Announcement Title'}</h3>
                  <span className={`text-sm font-medium ${getPriorityColor(formData.priority)}`}>
                    {formData.priority.charAt(0).toUpperCase() + formData.priority.slice(1)}
                  </span>
                </div>
                <p className="text-gray-700 whitespace-pre-wrap">
                  {formData.content || 'Your announcement content will appear here...'}
                </p>
                <div className="mt-3 text-sm text-gray-500">
                  Target: {formData.target_audience === 'all' ? 'All Users' : formData.target_audience.charAt(0).toUpperCase() + formData.target_audience.slice(1)}
                </div>
              </div>
            </div>

            {/* Warning for urgent announcements */}
            {formData.priority === 'urgent' && (
              <Alert>
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>
                  Urgent announcements will be highlighted prominently and may trigger immediate notifications to recipients.
                </AlertDescription>
              </Alert>
            )}

            {/* Action Buttons */}
            <div className="flex gap-3 pt-4">
              <Button
                onClick={handleSaveDraft}
                variant="outline"
                disabled={loading}
                className="flex items-center gap-2"
              >
                <Save className="h-4 w-4" />
                Save as Draft
              </Button>
              <Button
                onClick={handlePublish}
                disabled={loading}
                className="flex items-center gap-2"
              >
                <Send className="h-4 w-4" />
                {loading ? (isEditMode ? 'Updating...' : 'Publishing...') : (isEditMode ? 'Update & Publish' : 'Publish Announcement')}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default CreateAnnouncement;
