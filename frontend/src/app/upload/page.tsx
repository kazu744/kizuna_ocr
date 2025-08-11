"use client";
import { useState } from "react";

export default function UploadPage() {
  const [res, setRes] = useState<any>(null);

  const onChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const fd = new FormData();
    fd.append("new_owner_inkan", file);
    
    const r = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/upload`, {
        method: "POST",
        body: fd,
    });
    const json = await r.json();
    setRes(json);
  };

  return (
    <main style={{ padding: 16 }}>
        <h1>アップロード最小版</h1>
        <input type="file" accept="image/*,application/pdf" onChange={onChange} />
        <pre style={{ background: "#111", color: "#7CFC7C", padding: 12 }}>
            {res ? JSON.stringify(res, null, 2) : "← ファイル選んだら結果が出る"}
        </pre>
    </main>
  );
}