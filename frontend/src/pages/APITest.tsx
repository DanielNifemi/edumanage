import React, { useState } from 'react';
import { authAPI } from '@/lib/api';

const APITest: React.FC = () => {
  const [result, setResult] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const testLogin = async () => {
    setLoading(true);
    try {
      const response = await authAPI.login('test@example.com', 'password123');
      setResult(`Login Response: ${JSON.stringify(response, null, 2)}`);
    } catch (error) {
      setResult(`Login Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const testProfile = async () => {
    setLoading(true);
    try {
      const response = await authAPI.getProfile();
      setResult(`Profile Response: ${JSON.stringify(response, null, 2)}`);
    } catch (error) {
      setResult(`Profile Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const testRegister = async () => {
    setLoading(true);
    try {
      const userData = {
        username: 'testuser',
        email: 'test@example.com',
        password: 'password123',
        password_confirm: 'password123',
        first_name: 'Test',
        last_name: 'User',
        user_type: 'student' as const
      };
      const response = await authAPI.register(userData);
      setResult(`Register Response: ${JSON.stringify(response, null, 2)}`);
    } catch (error) {
      setResult(`Register Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-8">API Testing</h1>
      
      <div className="space-y-4 mb-8">
        <button
          onClick={testLogin}
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
        >
          Test Login API
        </button>
        
        <button
          onClick={testProfile}
          disabled={loading}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:opacity-50 ml-4"
        >
          Test Profile API
        </button>
        
        <button
          onClick={testRegister}
          disabled={loading}
          className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600 disabled:opacity-50 ml-4"
        >
          Test Register API
        </button>
      </div>

      {loading && <p className="text-blue-600">Loading...</p>}
      
      {result && (
        <div className="bg-white p-4 rounded border">
          <h3 className="font-bold mb-2">API Result:</h3>
          <pre className="whitespace-pre-wrap text-sm">{result}</pre>
        </div>
      )}
    </div>
  );
};

export default APITest;
