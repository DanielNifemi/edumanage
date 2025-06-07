import React from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const UIDiagnostic: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-8">UI Components Diagnostic</h1>
      
      <div className="space-y-6">
        <div>
          <h2 className="text-xl font-semibold mb-2">Button Component</h2>
          <Button>Test Button</Button>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-2">Input Component</h2>
          <Label htmlFor="test-input">Test Input</Label>
          <Input id="test-input" placeholder="Test input" />
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-2">Card Component</h2>
          <Card className="w-96">
            <CardHeader>
              <CardTitle>Test Card</CardTitle>
              <CardDescription>This is a test card description</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Card content goes here.</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default UIDiagnostic;
