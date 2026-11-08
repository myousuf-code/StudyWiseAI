import React, { createContext, useContext, useState, useEffect } from 'react';

export interface A11ySettings {
  fontSize: 'normal' | 'large' | 'xl';
  highContrast: boolean;
  dyslexicFont: boolean;
  lineSpacing: boolean;
  reducedMotion: boolean;
  ttsRate: number;
}

interface A11yContextType {
  settings: A11ySettings;
  updateSetting: <K extends keyof A11ySettings>(key: K, value: A11ySettings[K]) => void;
  resetSettings: () => void;
}

const defaultSettings: A11ySettings = {
  fontSize: 'normal',
  highContrast: false,
  dyslexicFont: false,
  lineSpacing: false,
  reducedMotion: false,
  ttsRate: 1.0,
};

const AccessibilityContext = createContext<A11yContextType | null>(null);

export const useAccessibility = (): A11yContextType => {
  const ctx = useContext(AccessibilityContext);
  if (!ctx) throw new Error('useAccessibility must be used within AccessibilityProvider');
  return ctx;
};

export const AccessibilityProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [settings, setSettings] = useState<A11ySettings>(() => {
    try {
      const saved = localStorage.getItem('a11y-settings');
      return saved ? { ...defaultSettings, ...JSON.parse(saved) } : defaultSettings;
    } catch {
      return defaultSettings;
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem('a11y-settings', JSON.stringify(settings));
    } catch {
      // localStorage may be unavailable
    }
    const html = document.documentElement;

    // Font size — mutual exclusion
    html.classList.remove('a11y-large-text', 'a11y-xl-text');
    if (settings.fontSize === 'large') html.classList.add('a11y-large-text');
    if (settings.fontSize === 'xl') html.classList.add('a11y-xl-text');

    // Boolean toggles
    html.classList.toggle('a11y-high-contrast', settings.highContrast);
    html.classList.toggle('a11y-dyslexic', settings.dyslexicFont);
    html.classList.toggle('a11y-line-spacing', settings.lineSpacing);
    html.classList.toggle('a11y-reduced-motion', settings.reducedMotion);
  }, [settings]);

  const updateSetting = <K extends keyof A11ySettings>(key: K, value: A11ySettings[K]) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const resetSettings = () => {
    setSettings(defaultSettings);
  };

  return (
    <AccessibilityContext.Provider value={{ settings, updateSetting, resetSettings }}>
      {children}
    </AccessibilityContext.Provider>
  );
};
