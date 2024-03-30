import logo from "./logo.svg";
import "./App.css";

import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import axios from "axios";
import { TextField } from "@mui/material";
import { Search } from "@mui/icons-material";

function createData(title, publishDateTime, thumbailUrl) {
  return { title, publishDateTime, thumbailUrl };
}

const url = "http://localhost:8000";


function App() {
  const [rows, setRows] = React.useState([]);
  const [currPage, setCurrPage] = React.useState(0);
  const [searchQuery, setSearchQuery] = React.useState("");
  const fetchVideoData = async () => {
    try {
      const finalUrl =
        searchQuery.length === 0
          ? `${url}/videos?page=${currPage + 1}&per_page=3`
          : `${url}/search?query=${searchQuery}&page=${currPage + 1}&per_page=3`;

      console.log(finalUrl);
      const res = await axios.get(finalUrl);
      if (res.data.video.length > 0) {
        setRows(res.data.video);
      } else {
        setCurrPage((currPage) => currPage - 1);
        alert("We are out of videos");
      }
      return res;
    } catch (err) {
      throw err;
    }
  };
  React.useEffect(() => {
    fetchVideoData();
  }, [currPage]);
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "25px" }}>
      <div
        style={{
          display: "flex",
          width: "100%",
          justifyContent: "center",
          gap: "10px",
        }}
      >
        <TextField
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button onClick={() => fetchVideoData()}>Search</button>
      </div>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell align="center">Thumbnail</TableCell>
              <TableCell align="center">Title</TableCell>
              <TableCell align="center">Published At</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {console.log(rows)}
            {rows.length > 0 &&
              rows.map((row) => (
                <TableRow
                  key={row.title + row.publishdatetime}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                >
                  <TableCell align="center">
                    <img
                      style={{ maxHeight: "50px", maxWidth: "50px" }}
                      src={row.thumbnailurl}
                    />
                  </TableCell>
                  <TableCell component="th" scope="row" align="center">
                    {row.title}
                  </TableCell>
                  <TableCell align="center">{row.publishdatetime}</TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      </TableContainer>
      <div
        style={{
          display: "flex",
          gap: "20px",
          width: "100%",
          justifyContent: "center",
        }}
      >
        <p
          onClick={() => {
            if (currPage > 0) {
              setCurrPage((currPage) => currPage - 1);
            }
          }}
        >
          Prev
        </p>
        <p>{currPage + 1}</p>
        <p onClick={() => setCurrPage((currPage) => currPage + 1)}>Next</p>
      </div>
    </div>
  );
}

export default App;
