#!/usr/bin/env python

# Copyright 2006 Google Inc. All Rights Reserved.
# Copyright 2017 Huan Wang (fredwanghuan@gmail.com)

import unittest
from s2 import *


class S2TestCase(unittest.TestCase):

    def testContainsIsWrappedCorrectly(self):
        london = S2LatLngRect(S2LatLng.FromDegrees(51.3368602, 0.4931979),
                              S2LatLng.FromDegrees(51.7323965, 0.1495211))
        e14lj = S2LatLngRect(S2LatLng.FromDegrees(51.5213527, -0.0476026),
                             S2LatLng.FromDegrees(51.5213527, -0.0476026))
        self.failUnless(london.Contains(e14lj))

    def testS2CellIdEqualsIsWrappedCorrectly(self):
        london = S2LatLng.FromDegrees(51.5001525, -0.1262355)
        cell = S2CellId.FromLatLng(london)
        same_cell = S2CellId.FromLatLng(london)
        self.assertEquals(cell, same_cell)

    def testS2CellIdComparsionIsWrappedCorrectly(self):
        london = S2LatLng.FromDegrees(51.5001525, -0.1262355)
        cell = S2CellId.FromLatLng(london)
        self.failUnless(cell < cell.next())
        self.failUnless(cell.next() > cell)

    def testS2HashingIsWrappedCorrectly(self):
        london = S2LatLng.FromDegrees(51.5001525, -0.1262355)
        cell = S2CellId.FromLatLng(london)
        same_cell = S2CellId.FromLatLng(london)
        # FIXME: Hash function is commented out in the SWIG, and broken.
        #self.assertEquals(hash(cell), hash(same_cell))

    def testCovererIsWrappedCorrectly(self):
        london = S2LatLngRect(S2LatLng.FromDegrees(51.3368602, 0.4931979),
                              S2LatLng.FromDegrees(51.7323965, 0.1495211))
        e14lj = S2LatLngRect(S2LatLng.FromDegrees(51.5213527, -0.0476026),
                             S2LatLng.FromDegrees(51.5213527, -0.0476026))
        coverer = S2RegionCoverer()
        covering = coverer.GetCovering(e14lj)
        for cellid in covering:
            self.failUnless(london.Contains(S2Cell(cellid)))

    def testGetEdgeNeighborsIsWrappedCorrectly(self):
        london = S2LatLngRect(S2LatLng.FromDegrees(51.3368602, 0.4931979),
                              S2LatLng.FromDegrees(51.7323965, 0.1495211))
        london_center = S2CellId.FromLatLng(london.GetCenter())
        london_neighbors = london_center.GetEdgeNeighbors()
        self.failUnlessEqual(len(london_neighbors), 4)
        for neighbor in london_neighbors:
            self.failIf(london_center.contains(neighbor))

    def testAssemblePolygonIsWrappedCorrectly(self):
        london = S2LatLngRect(S2LatLng.FromDegrees(51.3368602, 0.1495211),
                              S2LatLng.FromDegrees(51.7323965, 0.4931979))

        london_vertices = []
        for i in range(0, 4):
            london_vertices.append(london.GetVertex(i).ToPoint())
        london_vertices.append(london_vertices[0])  # to form a closed loop

        builder = S2PolygonBuilder(S2PolygonBuilderOptions.DIRECTED_XOR())
        for i in range(0, 4):
            builder.AddEdge(london_vertices[i], london_vertices[i + 1])
        returned = builder.AssemblePolygon()

        print "returned:", returned
        success, polygon, unused = returned
        bound = polygon.GetRectBound()
        self.failUnless(success)
        self.failUnless(polygon)
        self.failUnless(bound)
        self.failUnless(bound.is_valid())
        self.failIf(unused)


if __name__ == "__main__":
    unittest.main()
