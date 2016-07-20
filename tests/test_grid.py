from gldas.grid import GLDAS025Cellgrid


def test_GLDAS025_cell_grid():

    gldas = GLDAS025Cellgrid()
    assert gldas.activegpis.size == 1036800
    assert gldas.activegpis[153426] == 153426
    assert gldas.activearrcell[153426] == 1409
    assert gldas.activearrlat[153426] == -63.375
    assert gldas.activearrlon[153426] == 16.625
