import React from 'react';

interface FileUploaderProps {
  onChange: () => void;
}

const FileUploader: React.FunctionComponent<FileUploaderProps> = ({
  onChange,
}: FileUploaderProps) => {
  return (
    <>
      <label htmlFor="fileUploader">Last opp Excel-fil</label>
      <input
        type="file"
        name="fileUploader"
        accept=".xlsx, .xls"
        id="fileUploader"
        onChange={onChange}
      />
    </>
  );
};

export default FileUploader;
