import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import { 
  Plus, Edit, Trash2, Eye, Search, Filter,
  Megaphone, Clock, Users, AlertTriangle
} from "lucide-react";

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

const TeacherAnnouncements = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);
  const [filteredAnnouncements, setFilteredAnnouncements] = useState<Announcement[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterStatus, setFilterStatus] = useState("all");
  const [filterPriority, setFilterPriority] = useState("all");

  // Mock data - replace with API call
  useEffect(() => {
    const loadAnnouncements = async () => {
      try {
        setLoading(true);
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const mockAnnouncements: Announcement[] = [
          {
            id: 1,
            title: "Mid-term Exam Schedule",
            content: "The mid-term examinations will be conducted from March 15-22, 2025. Please ensure all students are prepared and have their admit cards ready.",
            priority: 'high',
            target_audience: 'students',
            is_published: true,
            created_at: '2025-03-01T10:00:00Z',
            updated_at: '2025-03-01T10:00:00Z',
            author_name: 'John Doe',
            views_count: 156
          },
          {
            id: 2,
            title: "Faculty Meeting - March 10",
            content: "All faculty members are required to attend the monthly meeting on March 10, 2025 at 2:00 PM in the conference room.",
            priority: 'normal',
            target_audience: 'teachers',
            is_published: true,
            created_at: '2025-02-28T14:30:00Z',
            updated_at: '2025-02-28T14:30:00Z',
            author_name: 'John Doe',
            views_count: 23
          },
          {
            id: 3,
            title: "Emergency Drill - Draft",
            content: "Emergency evacuation drill scheduled for next week. All staff and students should participate.",
            priority: 'urgent',
            target_audience: 'all',
            is_published: false,
            created_at: '2025-03-05T09:15:00Z',
            updated_at: '2025-03-05T09:15:00Z',
            author_name: 'John Doe',
            views_count: 0
          }
        ];
        
        setAnnouncements(mockAnnouncements);
      } catch (error) {
        console.error('Error loading announcements:', error);
        toast({
          title: "Error",
          description: "Failed to load announcements.",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
      }
    };

    loadAnnouncements();
  }, [toast]);

  // Filter announcements
  useEffect(() => {
    const filtered = announcements.filter(announcement => {
      const matchesSearch = announcement.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           announcement.content.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStatus = filterStatus === "all" || 
                           (filterStatus === "published" && announcement.is_published) ||
                           (filterStatus === "draft" && !announcement.is_published);
      const matchesPriority = filterPriority === "all" || announcement.priority === filterPriority;
      
      return matchesSearch && matchesStatus && matchesPriority;
    });
    
    setFilteredAnnouncements(filtered);
  }, [announcements, searchTerm, filterStatus, filterPriority]);

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

  const handleDeleteAnnouncement = async (id: number) => {
    try {
      // TODO: Replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setAnnouncements(prev => prev.filter(announcement => announcement.id !== id));
      toast({
        title: "Success",
        description: "Announcement deleted successfully.",
      });
    } catch (error) {
      console.error('Error deleting announcement:', error);
      toast({
        title: "Error",
        description: "Failed to delete announcement.",
        variant: "destructive",
      });
    }
  };

  const handleTogglePublish = async (id: number, currentStatus: boolean) => {
    try {
      // TODO: Replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setAnnouncements(prev => 
        prev.map(announcement => 
          announcement.id === id 
            ? { ...announcement, is_published: !currentStatus }
            : announcement
        )
      );
      
      toast({
        title: "Success",
        description: `Announcement ${currentStatus ? 'unpublished' : 'published'} successfully.`,
      });
    } catch (error) {
      console.error('Error updating announcement:', error);
      toast({
        title: "Error",
        description: "Failed to update announcement.",
        variant: "destructive",
      });
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="p-6">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-gray-200 rounded w-1/4"></div>
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="h-32 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Announcements</h1>
            <p className="text-gray-600 mt-1">Manage and share announcements with your audience</p>
          </div>
          <Button 
            onClick={() => navigate('/teacher/announcements/new')} 
            className="flex items-center gap-2"
          >
            <Plus className="h-4 w-4" />
            Create Announcement
          </Button>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Megaphone className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total</p>
                  <p className="text-2xl font-bold">{announcements.length}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Eye className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Published</p>
                  <p className="text-2xl font-bold">{announcements.filter(a => a.is_published).length}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-yellow-100 rounded-lg">
                  <Clock className="h-6 w-6 text-yellow-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Drafts</p>
                  <p className="text-2xl font-bold">{announcements.filter(a => !a.is_published).length}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Users className="h-6 w-6 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total Views</p>
                  <p className="text-2xl font-bold">{announcements.reduce((sum, a) => sum + (a.views_count || 0), 0)}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <Card>
          <CardContent className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <Label htmlFor="search">Search</Label>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                  <Input
                    id="search"
                    placeholder="Search announcements..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
              
              <div>
                <Label>Status</Label>
                <Select value={filterStatus} onValueChange={setFilterStatus}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="published">Published</SelectItem>
                    <SelectItem value="draft">Draft</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <Label>Priority</Label>
                <Select value={filterPriority} onValueChange={setFilterPriority}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Priorities</SelectItem>
                    <SelectItem value="urgent">Urgent</SelectItem>
                    <SelectItem value="high">High</SelectItem>
                    <SelectItem value="normal">Normal</SelectItem>
                    <SelectItem value="low">Low</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="flex items-end">
                <Button 
                  variant="outline" 
                  onClick={() => {
                    setSearchTerm('');
                    setFilterStatus('all');
                    setFilterPriority('all');
                  }}
                  className="flex items-center gap-2"
                >
                  <Filter className="h-4 w-4" />
                  Clear
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Announcements List */}
        <div className="space-y-4">
          {filteredAnnouncements.map((announcement) => (
            <Card key={announcement.id} className="hover:shadow-md transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-semibold">{announcement.title}</h3>
                      <Badge className={getPriorityColor(announcement.priority)}>
                        {announcement.priority}
                      </Badge>
                      <Badge className={getStatusColor(announcement.is_published)}>
                        {announcement.is_published ? 'Published' : 'Draft'}
                      </Badge>
                    </div>
                    
                    <p className="text-gray-600 mb-3 line-clamp-2">
                      {announcement.content}
                    </p>
                    
                    <div className="flex items-center gap-4 text-sm text-gray-500">
                      <span>Target: {announcement.target_audience}</span>
                      <span>•</span>
                      <span>Created: {new Date(announcement.created_at).toLocaleDateString()}</span>
                      {announcement.is_published && (
                        <>
                          <span>•</span>
                          <span>{announcement.views_count} views</span>
                        </>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex flex-col gap-2 ml-4">
                    <Button 
                      size="sm" 
                      variant="outline" 
                      className="flex items-center gap-1"
                      onClick={() => navigate(`/teacher/announcements/${announcement.id}`)}
                    >
                      <Eye className="h-3 w-3" />
                      View
                    </Button>
                    <Button 
                      size="sm" 
                      variant="outline" 
                      className="flex items-center gap-1"
                      onClick={() => navigate(`/teacher/announcements/${announcement.id}/edit`)}
                    >
                      <Edit className="h-3 w-3" />
                      Edit
                    </Button>
                    <Button 
                      size="sm" 
                      className="flex items-center gap-1"
                      onClick={() => handleTogglePublish(announcement.id, announcement.is_published)}
                    >
                      {announcement.is_published ? 'Unpublish' : 'Publish'}
                    </Button>
                    <Button 
                      size="sm" 
                      variant="destructive" 
                      className="flex items-center gap-1"
                      onClick={() => handleDeleteAnnouncement(announcement.id)}
                    >
                      <Trash2 className="h-3 w-3" />
                      Delete
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
          
          {filteredAnnouncements.length === 0 && (
            <Card>
              <CardContent className="p-12 text-center">
                <Megaphone className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No announcements found</h3>
                <p className="text-gray-600 mb-4">
                  {searchTerm || filterStatus !== 'all' || filterPriority !== 'all'
                    ? 'Try adjusting your filters to see more results.'
                    : 'Create your first announcement to get started.'
                  }
                </p>
                <Button onClick={() => navigate('/teacher/announcements/new')}>
                  <Plus className="h-4 w-4 mr-2" />
                  Create Announcement
                </Button>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default TeacherAnnouncements;
