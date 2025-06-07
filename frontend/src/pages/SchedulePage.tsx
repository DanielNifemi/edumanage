import React, { useEffect, useState, useCallback } from 'react';
import { schedulesAPI } from '@/lib/api'; // Import schedulesAPI
import { useAuth } from '@/contexts/useAuth';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { CalendarDays, AlertTriangle } from 'lucide-react';

// Placeholder types - replace with actual types from api.ts later if different
// Assuming ScheduleData from the backend matches this structure or is compatible.
// If api.ts exports a ScheduleData type for received schedules, import and use that.
interface ScheduleData {
  id: string;
  title: string;
  start_time: string;
  end_time: string;
  description?: string;
  course_name?: string;
  // Add any other fields that the backend /api/schedules/{userType}/{userId}/ might return
}

const SchedulePage: React.FC = () => {
  const { user } = useAuth();
  const [scheduleItems, setScheduleItems] = useState<ScheduleData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSchedule = useCallback(async () => {
    if (!user || !user.id || !user.role) {
      setError("User information is not available. Cannot fetch schedule.");
      setLoading(false);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      // Replace with actual API call
      const data = await schedulesAPI.getByUser(user.role, user.id);
      // Ensure data is an array, or adapt if the API returns a paginated response
      setScheduleItems(Array.isArray(data) ? data : (data.results || []));
    } catch (err) {
      console.error("Error fetching schedule:", err);
      setError('Failed to load schedule. Please try again later.');
    } finally {
      setLoading(false);
    }
  }, [user]); // Add user to dependency array

  useEffect(() => {
    fetchSchedule();
  }, [fetchSchedule]); // fetchSchedule already depends on user

  if (loading) {
    return <div className="p-6 text-center">Loading schedule...</div>;
  }

  if (error) {
    return (
      <div className="p-6">
        <Alert variant="destructive" className="mb-4">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
        <Button onClick={fetchSchedule}>Try Again</Button>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">My Schedule</h1>
        {/* Add "Create Event" button for relevant roles if applicable */}
      </div>

      {scheduleItems.length === 0 ? (
        <Card className="text-center">
          <CardHeader>
            <CardTitle>No Schedule Items</CardTitle>
          </CardHeader>
          <CardContent>
            <CalendarDays className="h-12 w-12 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600 dark:text-gray-400">Your schedule is currently empty.</p>
            {/* Optionally, add a link to view a full calendar or manage events */}
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {scheduleItems.map(item => (
            <Card key={item.id}>
              <CardHeader>
                <CardTitle>{item.title}</CardTitle>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {new Date(item.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} - 
                  {new Date(item.end_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  {item.course_name && ` | ${item.course_name}`}
                </p>
              </CardHeader>
              {item.description && (
                <CardContent>
                  <p className="text-sm text-gray-700 dark:text-gray-300">{item.description}</p>
                </CardContent>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default SchedulePage;
