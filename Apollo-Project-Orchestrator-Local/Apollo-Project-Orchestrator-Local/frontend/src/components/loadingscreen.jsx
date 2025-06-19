// src/components/LoadingScreen.jsx
import React from 'react';

const LoadingScreen = ({ message = "Carregando..." }) => {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      <div className="text-center">
        {/* Apollo Logo Animation */}
        <div className="mb-8">
          <div className="relative mx-auto w-20 h-20">
            <div className="absolute inset-0 rounded-full border-4 border-apollo-orange/20"></div>
            <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-apollo-orange animate-spin"></div>
            <div className="absolute inset-2 rounded-full bg-apollo-orange/10 flex items-center justify-center">
              <span className="text-apollo-orange font-bold text-xl">A</span>
            </div>
          </div>
        </div>

        {/* Loading Text */}
        <h2 className="text-xl font-semibold text-foreground mb-2">
          Apollo Project Orchestrator
        </h2>
        <p className="text-muted-foreground animate-pulse">
          {message}
        </p>

        {/* Loading Dots */}
        <div className="flex justify-center space-x-2 mt-6">
          <div className="w-2 h-2 bg-apollo-orange rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-apollo-orange rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
          <div className="w-2 h-2 bg-apollo-orange rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        </div>
      </div>
    </div>
  );
};

export default LoadingScreen;