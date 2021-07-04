import React from "react";
import sinon from "sinon";
import faker from "faker";
import { render, cleanup } from "@testing-library/react";
import { Button } from "../index";
import { ThemeProvider } from "@material-ui/core/styles";
import { theme } from "@/theme";

const sandbox = sinon.createSandbox();
const {
  lorem: { word },
} = faker;

describe("Button Unit Tests", () => {
  afterEach(() => {
    sandbox.verifyAndRestore();
    cleanup();
  });

  it("should render", () => {
    // Arrange
    sandbox.spy(React, "createElement");

    // Act
    const { container } = render(
      <ThemeProvider theme={theme}>
        <Button color="primary" name={word()} />
      </ThemeProvider>
    );

    // Assert
    expect(container.querySelector("button")).toBeInTheDocument();
  });
});
