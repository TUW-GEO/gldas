from gldas.grid import GLDAS025Cellgrid, GLDAS025LandGrid, subgrid4bbox


def test_GLDAS025_cell_grid():
    gldas = GLDAS025Cellgrid()
    assert gldas.activegpis.size == 1036800
    assert gldas.activegpis[153426] == 153426
    assert gldas.activearrcell[153426] == 1409
    assert gldas.activearrlat[153426] == -63.375
    assert gldas.activearrlon[153426] == 16.625


def test_GLDAS025LandGrid():
    gldas = GLDAS025LandGrid()
    assert gldas.activegpis.size == 243883
    assert gldas.activegpis[153426] == 810230
    assert gldas.activearrcell[153426] == 1720
    assert gldas.activearrlat[153426] == 50.625
    assert gldas.activearrlon[153426] == 57.625


def test_bbox_subgrid():
    bbox = (130.125, -29.875, 134.875, -25.125)  # bbox for cell 2244
    subgrid = subgrid4bbox(GLDAS025Cellgrid(), *bbox)
    assert subgrid == GLDAS025Cellgrid().subgrid_from_cells([2244])
