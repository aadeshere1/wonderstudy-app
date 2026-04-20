"use client";

import { useEffect, useState } from "react";
import { createStars } from "@/lib/utils/helpers";

export const StarsBackground = () => {
  const [stars, setStars] = useState<any[]>([]);

  useEffect(() => {
    setStars(createStars(90));
  }, []);

  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
      {stars.map((star, i) => (
        <div
          key={i}
          className="absolute star rounded-full animate-twinkle"
          style={{
            width: star.size,
            height: star.size,
            left: star.left,
            top: star.top,
            "--duration": star.duration,
          } as React.CSSProperties & { "--duration": string }}
        />
      ))}
    </div>
  );
};
