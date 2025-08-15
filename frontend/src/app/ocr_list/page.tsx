"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

interface OcrRecord {
  id: number;
  new_owner_name: string;
  new_owner_address_main: string;
  new_owner_address_street: string;
  new_owner_address_number: string;
  created_at: string;
  updated_at: string;
}

export default function OcrListPage() {
  const [ocrs, setOcrs] = useState<OcrRecord[]>([]);
  const [selected, setSelected] = useState<number[]>([]);
  const [selectAll, setSelectAll] = useState(false);

  useEffect(() => {
    fetch("http://localhost:8001/api/ocr?user_id=1")
      .then((res) => res.json())
      .then((data) => setOcrs(data));
  }, []);

  const handleSelectAll = () => {
    if (selectAll) {
        setSelected([]);
        setSelectAll(false);
    } else {
        setSelected(ocrs.map((ocr) => ocr.id));
        setSelectAll(true);
    }
  };

  const toggleSelect = (id: number) => {
    setSelected((prev) => {
      const newSelected = prev.includes(id)
        ? prev.filter((v) => v !== id)
        : [...prev, id];

        const allIds = ocrs.map((ocr) => ocr.id);
        setSelectAll(allIds.every((ocrId) => newSelected.includes(ocrId)));
        return newSelected;
    });
  };

  const deleteOcr = async (id: number) => {
    if (!confirm("本当に削除してもよろしいですか？")) return;
    const res = await fetch(`http://localhost:8001/api/ocr/${id}`, {
      method: "DELETE",
    });
    if (res.status === 204) {
      setOcrs((prev) => prev.filter((ocr) => ocr.id !== id));
      setSelected((prev) => prev.filter((ocrId) => ocrId !== id));
    } else if (res.status === 404) {
      alert("対象データが見つかりませんでした。");
    } else {
      alert("削除に失敗しました。");
    }
  };

  const handleExport = async () => {
    if (selected.length === 0) {
        alert("出力するレコードを選択してください");
        return;
    }
  const formData = new FormData();
  selected.forEach((id) => formData.append("ocr_ids", String(id)));

  const res = await fetch("http://localhost:8001/export", {
    method: "POST",
    body: formData,
  });

  const blob = await res.blob();
  const disposition = res.headers.get("Content-Disposition");
  let filename = "ocr_export.xlsx";
  if (disposition) {
    const match = disposition.match(/filename="?([^"]+)"?/);
    if (match && match[1]) filename = match[1];
  }

  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>登録情報取得一覧</h1>
      <table border={1} cellPadding={5}>
        <thead>
          <tr>
            <th>
              <input 
                type="checkbox"
                checked={selectAll}
                onChange={handleSelectAll}
               />
            </th>
            <th>ID</th>
            <th>氏名</th>
            <th>住所</th>
            <th>丁目</th>
            <th>番地</th>
            <th>作成日時</th>
            <th>更新日時</th>
            <th>削除</th>
          </tr>
        </thead>
        <tbody>
          {ocrs.map((ocr) => (
            <tr key={ocr.id}>
              <td>
                <input
                  type="checkbox"
                  checked={selected.includes(ocr.id)}
                  onChange={() => toggleSelect(ocr.id)}
                  />
              </td>
              <td><Link href={`/edit/${ocr.id}`}>{ocr.id}</Link></td>
              <td>{ocr.new_owner_name}</td>
              <td>{ocr.new_owner_address_main}</td>
              <td>{ocr.new_owner_address_street}</td>
              <td>{ocr.new_owner_address_number}</td>
              <td>{ocr.created_at}</td>
              <td>{ocr.updated_at}</td>
              <td>
                <button onClick={() => deleteOcr(ocr.id)}>削除</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <p>
        <button onClick={handleExport}>選択したデータをダウンロード</button>
      </p>

      <p>
        <Link href="/upload">アップロード画面に戻る</Link>
      </p>
    </div>
  );
}