// src/components/TitleHeadline.js
import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const TitleHeadline = () => {
  return (
    <Container className="mt-5">
      <Row>
        <Col className="text-center">
          <h1 className="display-4 fw-bold">
            The Money <br />
            <span className="ms-5">Printer</span>
          </h1>
        </Col>
      </Row>
    </Container>
  );
};

export default TitleHeadline;
