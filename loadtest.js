import http from "k6/http";

// global scope
const image = open("./test.jpg", "b");

export const options = {
  vus: 10,
  duration: "30s",
};

export default function () {

  const data = {
    file: http.file(image, "test.jpg"),
  };

  let res = http.post(
    "http://127.0.0.1:5001/predict",
    data
  );

  console.log(
    `STATUS=${res.status} TIME=${res.timings.duration}`
  );
}