"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";

export default function OcrEditPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [formData, setFormData] = useState({
    new_owner_name: "",
    new_owner_address_main: "",
    new_owner_address_street: "",
    new_owner_address_number: "",
  });

  useEffect(() => {
    if (!id) return;
    fetch(`http://localhost:8001/api/ocr/${id}`)
      .then((res) => res.json())
      .then((data) => {
        setFormData({
            new_owner_name: data.new_owner_name || "",
            new_owner_address_main: data.new_owner_address_main || "",
            new_owner_address_street: data.new_owner_address_street || "",
            new_owner_address_number: data.new_owner_address_number || "",
        });
      });
  }, [id]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const body = new FormData();
    Object.entries(formData).forEach(([key, value]) => {
        body.append(key, value);
    });

    const res = await fetch(`http://localhost:8001/api/ocr/${id}`, {
      method: "PUT",
      body,
    });

    if (res.ok) {
      alert("更新しました");
      router.push("/ocr_list");
    } else {
      alert("更新失敗しました")
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>データ編集</h1>
      <form onSubmit={handleSubmit}>
        <label>新所有者氏名</label><br />
        <input name="new_owner_name" value={formData.new_owner_name} onChange={handleChange} /><br />

        <label>新所有者住所</label><br />
        <input name="new_owner_address_main" value={formData.new_owner_address_main} onChange={handleChange} /><br />

        <label>新所有者丁目</label><br />
        <input name="new_owner_address_street" value={formData.new_owner_address_street} onChange={handleChange} /><br />

        <label>新所有者番地</label><br />
        <input name="new_owner_address_number" value={formData.new_owner_address_number} onChange={handleChange} /><br />

        <button type="submit">更新</button>
        
      </form>
      
      <p>
        <Link href="/ocr_list">一覧へ戻る</Link>
      </p>
    </div>
  );
}
