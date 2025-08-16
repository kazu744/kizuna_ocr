"use client";

import { useState } from "react"
import Link from "next/link";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0])
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!file) {
      setMessage("ファイルを選択してください");
      return;
    }

    const formData = new FormData();
    formData.append("new_owner_inkan", file);

    try {
      const res = await fetch("http://localhost:8001/upload", {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        setMessage("アップロードが完了しました。");
        setFile(null);
        (e.target as HTMLFormElement).reset();
      } else {
        const err = await res.json();
        setMessage(`エラー: ${err.detail}`);
      }
    } catch (error: any) {
      setMessage(`アップロードが失敗しました: ${error.message || error}`)
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>書類アップロード</h1>
      <p>新所有者印鑑証明 ※印影は隠してください</p>
      
      <form onSubmit={handleSubmit} encType="multipart/form-data">
        <p>
          <input type="file"
          name="new_owner_inkan"
          accept=".jpg,.jpeg,.png,.pdf"
          onChange={handleFileChange}
          />
        </p>
        <p>
          <button type="submit">アップロード</button>
        </p>
      </form>

      {message && <p>{message}</p> }

      <p>
        <Link href="/ocr_list">一覧へ</Link>
      </p>
    </div>
  );
}