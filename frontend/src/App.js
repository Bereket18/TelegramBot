import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [currentView, setCurrentView] = useState('main');
  const [selectedPortal, setSelectedPortal] = useState('');
  const [loginData, setLoginData] = useState({ username: '', password: '' });
  const [loginStatus, setLoginStatus] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const backendUrl = process.env.REACT_APP_BACKEND_URL;

  const portals = [
    {
      id: 'admin',
      title: 'Admin Portal',
      titleAm: 'የአስተዳደር መግቢያ',
      description: 'Manage the entire system and oversee all operations',
      descriptionAm: 'መላውን ስርዓት ማስተዳደር እና ሁሉንም ተግባራት መቆጣጠር',
      gradient: 'from-blue-600 to-blue-800',
      icon: '👨‍💼'
    },
    {
      id: 'teacher',
      title: 'Teachers Portal',
      titleAm: 'የመምህራን መግቢያ',
      description: 'Access teaching resources and student management',
      descriptionAm: 'የማስተማሪያ ግብዓቶችን እና የተማሪ አስተዳደርን ማግኘት',
      gradient: 'from-green-600 to-green-800',
      icon: '👨‍🏫'
    },
    {
      id: 'student',
      title: 'Students Portal',
      titleAm: 'የተማሪዎች መግቢያ',
      description: 'Embark on your journey with the Divine Revelation as your guide',
      descriptionAm: 'Allah ገለጣ እንደ መሪ ተጠቅመው ጉዞዎን ጀምሩ',
      gradient: 'from-teal-600 to-teal-800',
      icon: '👨‍🎓'
    }
  ];

  const handlePortalSelect = (portalId) => {
    setSelectedPortal(portalId);
    setCurrentView('login');
    setLoginData({ username: '', password: '' });
    setLoginStatus('');
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setLoginStatus('');

    try {
      const response = await fetch(`${backendUrl}/api/login/${selectedPortal}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
      });

      const result = await response.json();
      
      if (result.success) {
        setLoginStatus('success');
        setTimeout(() => {
          setCurrentView('dashboard');
        }, 1500);
      } else {
        setLoginStatus('error');
      }
    } catch (error) {
      console.error('Login error:', error);
      setLoginStatus('error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleBackToMain = () => {
    setCurrentView('main');
    setSelectedPortal('');
    setLoginData({ username: '', password: '' });
    setLoginStatus('');
  };

  const getCurrentPortal = () => {
    return portals.find(p => p.id === selectedPortal);
  };

  const renderMainPortals = () => (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12 pt-8">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-gold to-yellow-500 rounded-full mb-6 shadow-lg">
            <span className="text-3xl">🕌</span>
          </div>
          <h1 className="text-4xl font-bold text-white mb-2">
            Al-Muhsin Quran Academy
          </h1>
          <h2 className="text-2xl text-amber-300 font-medium mb-4">
            ኣል-ሙሕሲን የቁርኣን ኣካዳሚ
          </h2>
          <p className="text-gray-300 text-lg">
            Choose your portal to access the learning system
          </p>
          <p className="text-gray-300 text-sm mt-2">
            የትምህርት ስርዓቱን ለመጠቀም የእርስዎን መግቢያ ይምረጡ
          </p>
        </div>

        {/* Portal Cards */}
        <div className="grid md:grid-cols-3 gap-8">
          {portals.map((portal) => (
            <div
              key={portal.id}
              className="group relative overflow-hidden rounded-2xl bg-white/10 backdrop-blur-sm border border-white/20 hover:border-white/30 transition-all duration-300 hover:scale-105 hover:shadow-2xl cursor-pointer"
              onClick={() => handlePortalSelect(portal.id)}
            >
              <div className={`absolute inset-0 bg-gradient-to-br ${portal.gradient} opacity-20 group-hover:opacity-30 transition-opacity duration-300`}></div>
              
              <div className="relative p-8 text-center">
                <div className="text-6xl mb-6 group-hover:scale-110 transition-transform duration-300">
                  {portal.icon}
                </div>
                
                <h3 className="text-2xl font-bold text-white mb-2">
                  {portal.title}
                </h3>
                <h4 className="text-lg text-amber-300 mb-4 font-medium">
                  {portal.titleAm}
                </h4>
                
                <p className="text-gray-300 text-sm mb-4 leading-relaxed">
                  {portal.description}
                </p>
                <p className="text-gray-400 text-xs leading-relaxed">
                  {portal.descriptionAm}
                </p>
                
                <div className="mt-8">
                  <button className="bg-white/20 hover:bg-white/30 text-white px-8 py-3 rounded-xl font-semibold transition-all duration-300 backdrop-blur-sm border border-white/30 hover:border-white/50 group-hover:shadow-lg">
                    Enter Portal
                  </button>
                </div>
              </div>
              
              <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-white/50 to-transparent"></div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="text-center mt-16 pb-8">
          <div className="bg-blue-900/30 backdrop-blur-sm rounded-2xl p-6 border border-blue-500/20">
            <p className="text-blue-200 text-sm leading-relaxed">
              <span className="font-medium">"وَلَقَدْ يَسَّرْنَا الْقُرْآنَ لِلذِّكْرِ فَهَلْ مِن مُّدَّكِرٍ"</span>
            </p>
            <p className="text-blue-300 text-xs mt-2">
              "ቁርኣንን ለመዘከር አስቀል አድርገነዋል፤ ከሚዘከር ማንኛውም ሰው አለን?"
            </p>
            <p className="text-blue-400 text-xs mt-3 font-medium">
              © 1445H Al-Muhsin Quran Academy. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderLogin = () => {
    const portal = getCurrentPortal();
    if (!portal) return null;

    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          {/* Back Button */}
          <button
            onClick={handleBackToMain}
            className="mb-6 flex items-center text-white/70 hover:text-white transition-colors duration-200"
          >
            <span className="mr-2">←</span>
            Back to Portals
          </button>

          {/* Login Card */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 p-8 shadow-2xl">
            <div className="text-center mb-8">
              <div className="text-5xl mb-4">{portal.icon}</div>
              <h2 className="text-2xl font-bold text-white mb-2">
                {portal.title}
              </h2>
              <h3 className="text-lg text-amber-300 font-medium">
                {portal.titleAm}
              </h3>
            </div>

            <form onSubmit={handleLogin} className="space-y-6">
              <div>
                <input
                  type="text"
                  placeholder="Username"
                  value={loginData.username}
                  onChange={(e) => setLoginData({...loginData, username: e.target.value})}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:border-white/40 focus:bg-white/15 transition-all duration-200"
                  required
                />
              </div>
              
              <div>
                <input
                  type="password"
                  placeholder="Password"
                  value={loginData.password}
                  onChange={(e) => setLoginData({...loginData, password: e.target.value})}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:border-white/40 focus:bg-white/15 transition-all duration-200"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className={`w-full py-3 rounded-xl font-semibold transition-all duration-300 ${
                  isLoading 
                    ? 'bg-gray-600 cursor-not-allowed' 
                    : `bg-gradient-to-r ${portal.gradient} hover:shadow-lg hover:scale-105`
                } text-white`}
              >
                {isLoading ? 'Signing In...' : 'Enter'}
              </button>
            </form>

            {/* Status Messages */}
            {loginStatus === 'success' && (
              <div className="mt-4 p-3 bg-green-500/20 border border-green-500/30 rounded-lg text-green-300 text-center">
                Login successful! Redirecting...
              </div>
            )}
            
            {loginStatus === 'error' && (
              <div className="mt-4 p-3 bg-red-500/20 border border-red-500/30 rounded-lg text-red-300 text-center">
                Invalid credentials. Please try again.
              </div>
            )}

            {/* Demo Credentials */}
            <div className="mt-6 p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
              <p className="text-blue-300 text-sm font-medium mb-2">Demo Credentials:</p>
              <p className="text-blue-200 text-xs">
                Username: <span className="font-mono bg-blue-900/30 px-2 py-1 rounded">{portal.id}</span>
              </p>
              <p className="text-blue-200 text-xs mt-1">
                Password: <span className="font-mono bg-blue-900/30 px-2 py-1 rounded">{portal.id}123</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderDashboard = () => {
    const portal = getCurrentPortal();
    if (!portal) return null;

    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="flex items-center justify-between mb-8 pt-4">
            <button
              onClick={handleBackToMain}
              className="flex items-center text-white/70 hover:text-white transition-colors duration-200"
            >
              <span className="mr-2">←</span>
              Back to Portals
            </button>
            
            <div className="text-center">
              <h1 className="text-2xl font-bold text-white">
                Welcome to {portal.title}
              </h1>
              <p className="text-amber-300">{portal.titleAm}</p>
            </div>
            
            <div className="w-20"></div>
          </div>

          {/* Dashboard Content */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 p-8">
            <div className="text-center">
              <div className="text-6xl mb-6">{portal.icon}</div>
              <h2 className="text-3xl font-bold text-white mb-4">
                {portal.title} Dashboard
              </h2>
              <p className="text-gray-300 mb-8">
                You have successfully logged into the {portal.title.toLowerCase()}.
              </p>
              
              <div className="grid md:grid-cols-2 gap-6 mt-8">
                <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                  <h3 className="text-xl font-semibold text-white mb-2">Quick Actions</h3>
                  <p className="text-gray-300 text-sm">Access frequently used features</p>
                </div>
                
                <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                  <h3 className="text-xl font-semibold text-white mb-2">Recent Activity</h3>
                  <p className="text-gray-300 text-sm">View your recent interactions</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="App">
      {currentView === 'main' && renderMainPortals()}
      {currentView === 'login' && renderLogin()}
      {currentView === 'dashboard' && renderDashboard()}
    </div>
  );
};

export default App;