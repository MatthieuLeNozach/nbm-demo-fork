import { Pagination } from "@material-ui/lab";
import React, { useEffect, useState } from "react";
import useSWR from "swr";
import { useAuth } from "@/components/Providers/AuthProvider";

interface Props {
  endpoint: string;
  numberByPage: number;
  personal: boolean;
  onListChange(Array): void;
}

const CustomPagination: React.FC<Props> = ({
  endpoint,
  numberByPage,
  onListChange,
  personal,
}) => {
  const { accessToken, user } = useAuth();

  const [currentPage, setCurrentPage] = useState<number>(1);
  const [pagesNumber, setPagesNumber] = useState<number>(0);
  const [firstEventSent, setFirstEventSent] = useState<boolean>(false);
  const [baseEndpoint, setBaseEndpoint] = useState<string>(`/${endpoint}`);
  const [paginationEndpoint, setPaginationEndpoint] = useState<string | null>(
    null
  );

  const { data: count } = useSWR([
    `/utils/${personal ? "personal-" : ""}count`,
    accessToken,
  ]);

  const { data: modelsList } = useSWR([paginationEndpoint, accessToken]);

  const pageChange = (e, value) => {
    setCurrentPage(value);
    const skip = (value - 1) * numberByPage;
    const firstCharacter = baseEndpoint.includes("?") ? "&" : "?";
    setPaginationEndpoint(
      `${baseEndpoint}${firstCharacter}skip=${skip}&limit=${numberByPage}`
    );
  };

  useEffect(() => {
    if (count && !isNaN(count[endpoint])) {
      setPagesNumber(Math.ceil(count[endpoint] / numberByPage));
    } else {
      setPagesNumber(0);
    }
  }, [count]);

  useEffect(() => {
    setBaseEndpoint(
      personal && user ? `/${endpoint}?created_by=${user.id}` : `/${endpoint}`
    );
  }, [personal, user, endpoint]);

  useEffect(() => {
    pageChange(null, 1);
  }, [baseEndpoint]);

  useEffect(() => {
    onListChange(modelsList);
  }, [modelsList]);

  if (firstEventSent === false) {
    pageChange(null, 1);
    setFirstEventSent(true);
  }

  return (
    <>
      {pagesNumber > 0 && (
        <Pagination
          count={pagesNumber}
          page={currentPage}
          onChange={pageChange}
          showFirstButton
          showLastButton
        />
      )}
    </>
  );
};

export default CustomPagination;
