## Copyright (C) 2011 Stellenbosch University
##
## This file is part of SUCEM.
##
## SUCEM is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## SUCEM is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with SUCEM. If not, see <http://www.gnu.org/licenses/>. 
##
## Contact: cemagga@gmail.com 
# Authors:
# Neilen Marais <nmarais@gmail.com>
import dolfin
import numpy as N

def listmesh_2_dolfin_mesh(listmesh, reorder=False):
    """Setup dolfin mesh using node and tet data from listmesh

    If parameter reorder is set to True, the order() method will be
    called on the dolfin mesh to sort the mesh according to UFC
    specifications.
    """
    dm = dolfin.Mesh()
    me = dolfin.MeshEditor()
    me.open(dm, 'tetrahedron', 3, 3)
    me.init_vertices(len(listmesh['Nodes']))
    me.init_cells(len(listmesh['ElementNodes']))
    dm.coordinates()[:,:] = listmesh['Nodes']
    #dm.cells()[:,:] = listmesh['ElementNodes']
    for i, enodes in enumerate(listmesh['ElementNodes']):
        me.add_cell(i, *enodes)
    me.close()
    if reorder: dm.order()
    return dm

def dolfin_mesh_2_listmesh(dolfin_mesh):
    """Convert a dolfin mesh to a listmesh format (as in PhD code)

    returns listmesh, a dict of seqs (i.e. lists) of mesh
    information. I think PhD code expects them to be arrays
    actually. This function only sets the keys 'Nodes' with the mesh
    node (i.e. vertex) coordinates and 'ElementNodes' with the
    tetrahedral element node numbers.
    """
    listmesh = {}
    listmesh['Nodes'] = dolfin_mesh.coordinates().copy()
    listmesh['ElementNodes'] = N.array(dolfin_mesh.cells(),
                                       dtype=N.int32, copy=True)
    return listmesh

def femmesh_reader_2_dolfin_mesh(femmesh_reader, reorder=True):
    """Convert a MeshIO.FemmeshReader object to a dolfin mesh"""
    if not femmesh_reader.read: femmesh_reader.read_meshfile()
    listmesh = dict(
        FemmeshFilename=femmesh_reader.get_mesh_filename(),
        FemmeshDir = femmesh_reader.get_mesh_dirname(),
        Nodes=femmesh_reader.get_nodes(),
        ElementNodes=femmesh_reader.get_tet_nodes())
    return listmesh_2_dolfin_mesh(listmesh, reorder=reorder)

