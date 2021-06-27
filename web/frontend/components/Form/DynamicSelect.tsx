import React, { useEffect, useState } from "react";
import { useAuth } from "@/components/Providers/AuthProvider";
import useSWR from "swr";
import Select from "react-select";
import { Site } from "@/models/site";
import { SelectOption } from "@/models/utils";

const customSelectStyles = {
  option: (provided) => ({
    ...provided,
    color: "black",
  }),
  container: (provided) => {
    return {
      ...provided,
      position: "relative",
      top: "12px",
      marginBottom: "20px",
    };
  },
  control: (provided) => {
    return {
      ...provided,
      backgroundColor: "inherit",
      border: "1px solid rgba(0, 0, 0, 0.23)",
    };
  },
  valueContainer: (provided) => {
    return { ...provided, padding: 13 };
  },
  singleValue: (provided) => {
    return { ...provided, color: "white" };
  },
  input: (provided) => {
    return { ...provided, color: "white" };
  },
  placeholder: (provided) => {
    return { ...provided, color: "white" };
  },
};

interface DynamicSelectProps {
  placeholder: string;
  columnName: string;
  endpoint: string;
  optionalText?: string;
  defaultValue?: SelectOption;
  onChange?(option: SelectOption | null): void;
}

const DynamicSelect: React.FC<DynamicSelectProps> = ({
  placeholder,
  columnName,
  endpoint,
  optionalText,
  defaultValue,
  onChange,
}) => {
  const { accessToken } = useAuth();

  const requestTimeoutMilliseconds = 1000;
  const [requestTimeout, setRequestTimeout] = useState<null | ReturnType<
    typeof setTimeout
  >>(null);

  const [selectedOption, _setSelectedOption] = useState<SelectOption | null>(
    defaultValue || null
  );
  const setSelectedOption = (option: SelectOption | null) => {
    if (option?.value === 0) {
      option = null;
    }
    _setSelectedOption(option);
    if (typeof onChange === "function") {
      onChange(option);
    }
  };

  const [modelsList, setModelsList] = useState<Array<Site>>([]);
  const [requestParameter, setRequestParameter] = useState<string>("");
  const { data: requestList } = useSWR([
    `${endpoint}${requestParameter}`,
    accessToken,
  ]);
  const setSiteInput = (input) => {
    if (requestTimeout !== null) {
      clearTimeout(requestTimeout);
      setRequestTimeout(null);
    }
    setRequestTimeout(
      setTimeout(() => {
        setRequestParameter(input.length > 3 ? `?${columnName}=${input}` : "");
        setRequestTimeout(null);
      }, requestTimeoutMilliseconds)
    );
  };
  useEffect(() => {
    if (Array.isArray(requestList)) {
      const values = [];
      if (optionalText) {
        const unselectOption = { id: 0 };
        unselectOption[columnName] = optionalText;
        values.push(unselectOption);
      }
      values.push(...requestList);
      setModelsList(values);
    }
  }, [requestList]);

  return (
    <Select
      placeholder={placeholder}
      styles={customSelectStyles}
      instanceId={`${endpoint}-select`}
      defaultValue={selectedOption}
      onChange={setSelectedOption}
      onInputChange={setSiteInput}
      options={
        Array.isArray(modelsList)
          ? modelsList.map((model) => ({
              value: model.id,
              label: model[columnName],
            }))
          : []
      }
    />
  );
};

export default DynamicSelect;
