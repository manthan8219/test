import { useState, useEffect } from "react";

const useGetTodos = (url) => {
  console.log("Entering to get the todos")
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const fetchData = async () => {
    try {
      const response = await fetch(url, { method: "GET" });
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    fetchData();
  }, [url]);

  return [data, loading,fetchData];
};

export default useGetTodos;
