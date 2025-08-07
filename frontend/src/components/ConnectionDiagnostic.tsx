import React, { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle, XCircle, Wifi, WifiOff } from 'lucide-react';

interface ConnectionStatus {
  backend: 'checking' | 'connected' | 'failed';
  auth: 'checking' | 'connected' | 'failed' | 'unauthenticated';
  ai: 'checking' | 'connected' | 'failed';
  cors: 'checking' | 'working' | 'blocked';
}

export default function ConnectionDiagnostic() {
  const [status, setStatus] = useState<ConnectionStatus>({
    backend: 'checking',
    auth: 'checking',
    ai: 'checking',
    cors: 'checking'
  });
  const [logs, setLogs] = useState<string[]>([]);
  const [showDiagnostic, setShowDiagnostic] = useState(false);

  const log = (message: string) => {
    setLogs(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
    console.log('🔍 Connection Diagnostic:', message);
  };

  const testBackendConnection = async () => {
    try {
      log('Testing backend connection...');
      const response = await fetch('https://onlypans.onrender.com/api/health/', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      
      if (response.ok) {
        const data = await response.json();
        log(`✅ Backend connected: ${data.message}`);
        setStatus(prev => ({ ...prev, backend: 'connected' }));
        return true;
      } else {
        log(`❌ Backend error: HTTP ${response.status}`);
        setStatus(prev => ({ ...prev, backend: 'failed' }));
        return false;
      }
    } catch (error: any) {
      log(`❌ Backend connection failed: ${error.message}`);
      setStatus(prev => ({ ...prev, backend: 'failed' }));
      return false;
    }
  };

  const testCORSConnection = async () => {
    try {
      log('Testing CORS configuration...');
      const response = await fetch('https://onlypans.onrender.com/api/cors-test/', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      
      if (response.ok) {
        const data = await response.json();
        log(`✅ CORS working: ${data.message}`);
        setStatus(prev => ({ ...prev, cors: 'working' }));
        return true;
      } else {
        log(`⚠️ CORS test endpoint returned: ${response.status}`);
        setStatus(prev => ({ ...prev, cors: 'working' })); // Still working if we get a response
        return true;
      }
    } catch (error: any) {
      if (error.message.includes('CORS')) {
        log(`❌ CORS blocked: ${error.message}`);
        setStatus(prev => ({ ...prev, cors: 'blocked' }));
      } else {
        log(`❌ CORS test failed: ${error.message}`);
        setStatus(prev => ({ ...prev, cors: 'blocked' }));
      }
      return false;
    }
  };

  const testAuthConnection = async () => {
    try {
      log('Testing authentication...');
      const token = localStorage.getItem('token');
      
      if (!token) {
        log('⚠️ No auth token found - user not logged in');
        setStatus(prev => ({ ...prev, auth: 'unauthenticated' }));
        return false;
      }

      const response = await fetch('https://onlypans.onrender.com/api/auth/profile/', {
        method: 'GET',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        log(`✅ Authentication working: ${data.username || 'User authenticated'}`);
        setStatus(prev => ({ ...prev, auth: 'connected' }));
        return true;
      } else if (response.status === 401) {
        log('⚠️ Auth token expired - user needs to log in');
        setStatus(prev => ({ ...prev, auth: 'unauthenticated' }));
        return false;
      } else {
        log(`❌ Auth error: HTTP ${response.status}`);
        setStatus(prev => ({ ...prev, auth: 'failed' }));
        return false;
      }
    } catch (error: any) {
      log(`❌ Auth test failed: ${error.message}`);
      setStatus(prev => ({ ...prev, auth: 'failed' }));
      return false;
    }
  };

  const testAIConnection = async () => {
    try {
      log('Testing AI service...');
      const response = await fetch('https://onlypans.onrender.com/api/ai/status/', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.available) {
          log(`✅ AI service available: ${data.message}`);
          setStatus(prev => ({ ...prev, ai: 'connected' }));
          return true;
        } else {
          log(`❌ AI service unavailable: ${data.message}`);
          setStatus(prev => ({ ...prev, ai: 'failed' }));
          return false;
        }
      } else {
        log(`❌ AI status error: HTTP ${response.status}`);
        setStatus(prev => ({ ...prev, ai: 'failed' }));
        return false;
      }
    } catch (error: any) {
      log(`❌ AI test failed: ${error.message}`);
      setStatus(prev => ({ ...prev, ai: 'failed' }));
      return false;
    }
  };

  const runFullDiagnostic = async () => {
    log('🚀 Starting connection diagnostic...');
    
    // Reset status
    setStatus({
      backend: 'checking',
      auth: 'checking',
      ai: 'checking',
      cors: 'checking'
    });

    // Run tests in sequence
    const backendOK = await testBackendConnection();
    const corsOK = await testCORSConnection();
    
    if (backendOK && corsOK) {
      await testAuthConnection();
      await testAIConnection();
    } else {
      setStatus(prev => ({ 
        ...prev, 
        auth: 'failed',
        ai: 'failed'
      }));
    }

    log('🏁 Diagnostic complete');
  };

  useEffect(() => {
    // Auto-run diagnostic on mount
    runFullDiagnostic();
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'connected':
      case 'working':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'failed':
      case 'blocked':
        return <XCircle className="w-5 h-5 text-red-500" />;
      case 'unauthenticated':
        return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      default:
        return <div className="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected':
      case 'working':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'failed':
      case 'blocked':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'unauthenticated':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      default:
        return 'text-blue-600 bg-blue-50 border-blue-200';
    }
  };

  return (
    <div className="fixed top-4 right-4 z-50">
      {/* Connection Status Indicator */}
      <div 
        className="bg-white rounded-lg shadow-lg border-2 p-3 cursor-pointer"
        onClick={() => setShowDiagnostic(!showDiagnostic)}
      >
        <div className="flex items-center space-x-2">
          {status.backend === 'connected' && status.cors === 'working' ? (
            <Wifi className="w-5 h-5 text-green-500" />
          ) : (
            <WifiOff className="w-5 h-5 text-red-500" />
          )}
          <span className="text-sm font-medium">
            {status.backend === 'connected' && status.cors === 'working' ? 'Connected' : 'Connection Issues'}
          </span>
        </div>
      </div>

      {/* Diagnostic Panel */}
      {showDiagnostic && (
        <div className="absolute top-16 right-0 bg-white rounded-lg shadow-xl border-2 p-4 w-96 max-h-96 overflow-y-auto">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Connection Diagnostic</h3>
            <button
              onClick={runFullDiagnostic}
              className="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600"
            >
              Retest
            </button>
          </div>

          {/* Status Items */}
          <div className="space-y-3 mb-4">
            <div className={`flex items-center justify-between p-2 rounded border ${getStatusColor(status.backend)}`}>
              <span className="text-sm font-medium">Backend</span>
              {getStatusIcon(status.backend)}
            </div>
            
            <div className={`flex items-center justify-between p-2 rounded border ${getStatusColor(status.cors)}`}>
              <span className="text-sm font-medium">CORS</span>
              {getStatusIcon(status.cors)}
            </div>
            
            <div className={`flex items-center justify-between p-2 rounded border ${getStatusColor(status.auth)}`}>
              <span className="text-sm font-medium">Authentication</span>
              {getStatusIcon(status.auth)}
            </div>
            
            <div className={`flex items-center justify-between p-2 rounded border ${getStatusColor(status.ai)}`}>
              <span className="text-sm font-medium">AI Service</span>
              {getStatusIcon(status.ai)}
            </div>
          </div>

          {/* Action Buttons */}
          {status.cors === 'blocked' && (
            <div className="bg-red-50 border border-red-200 rounded p-3 mb-4">
              <p className="text-sm text-red-600 mb-2">
                <strong>CORS Issue Detected!</strong>
              </p>
              <p className="text-xs text-red-500">
                The frontend cannot communicate with the backend due to CORS policy restrictions.
              </p>
            </div>
          )}

          {status.auth === 'unauthenticated' && (
            <div className="bg-yellow-50 border border-yellow-200 rounded p-3 mb-4">
              <p className="text-sm text-yellow-600 mb-2">
                <strong>Login Required</strong>
              </p>
              <p className="text-xs text-yellow-500">
                Please log in to access AI features.
              </p>
            </div>
          )}

          {/* Logs */}
          <div className="border-t pt-3">
            <h4 className="text-sm font-medium mb-2">Diagnostic Logs:</h4>
            <div className="bg-gray-50 rounded p-2 text-xs max-h-32 overflow-y-auto">
              {logs.map((log, index) => (
                <div key={index} className="text-gray-600 mb-1">
                  {log}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
