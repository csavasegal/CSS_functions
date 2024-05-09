import matplotlib.pyplot as plt
from nilearn import surface
from nilearn import datasets
fsaverage = datasets.fetch_surf_fsaverage()
from nilearn.plotting import plot_surf_roi, view_surf, plot_stat_map
import numpy as np
import nibabel as nib
from matplotlib.pyplot import figure



surface_data = {}
surface_data['surf_mesh_left'] = fsaverage.infl_left
surface_data['surf_mesh_right'] = fsaverage.infl_right

def color_rois(values):
    """
    This function assumes you are passing a vector "values" with the same length as the number of nodes in the atlas.
    """
    data_dir = data_dir = '/dartfs/rc/lab/F/FinnLab/clara/K99_EventSeg/data/'
    atlas_fname = (data_dir + '_masks/'+ 'Schaefer2018_100Parcels_7Networks_order_FSLMNI152_1mm.nii.gz')
    schaeffer = nib.load(atlas_fname)
    schaeffer100_data = schaeffer.get_fdata()
    img = np.zeros(schaeffer100_data.shape)
    for roi in range(len(values)):
        itemindex = np.where(schaeffer100_data==roi+1) # find voxels in this node (subtract 1 to account for zero-indexing)
        img[itemindex] = values[roi] # color them by the desired value 
    affine = schaeffer.affine
    img_nii = nib.Nifti1Image(img, affine)
    
    return img_nii
def plot_surf_left(surf_mesh, view, fig, axes, cmap,colorbar,vmin, vmax,darkness, threshold):
    img = plot_surf_roi(surf_mesh, 
                        roi_map=surface_data['comp_labels'],
                        view = view,
                        cmap=cmap,
                        vmax=vmax, 
                        hemi='left',
                        threshold=threshold,

                        #vmin=np.nanmin(surface_data['comp_labels']),
                        vmin=vmin,
                        bg_map=fsaverage.sulc_left,
                        darkness=darkness,
                        bg_on_data=True,
                        title='',
                        figure = fig,
                        axes=axes,
                        colorbar=colorbar)
    return img

def plot_surf_right(surf_mesh, view, fig, axes, cmap,colorbar,vmin, vmax,darkness, threshold):
    img = plot_surf_roi(surf_mesh, 
                        roi_map=surface_data['comp_labels'],
                        view = view,
                        cmap=cmap,
                        vmax=vmax, 
                        vmin=vmin,
                        hemi='right',
                        threshold=threshold,
                        #vmin=np.nanmin(surface_data['comp_labels']),
                        bg_map=fsaverage.sulc_right,
                        darkness=darkness,
                        bg_on_data=True,
                        title='',
                        figure = fig,
                        axes=axes,
                        colorbar=colorbar)
    return img


def plot_brain_surface(volume, surf_mesh, hemisphere, cmap, vmin, vmax, darkness):
    """
    Plot brain surfaces for each view ('lateral' and 'medial').

    :param volume: Volume data to plot.
    :param surf_mesh: Surface mesh data.
    :param hemisphere: Hemisphere ('left' or 'right').
    :param cmap: Colormap for the plot.
    :param vmin: Minimum value for colormap scaling.
    :param vmax: Maximum value for colormap scaling.
    :param darkness: Darkness parameter for the plot.
    """
    texture = surface.vol_to_surf(volume, surf_mesh, interpolation='nearest', radius=1, n_samples=1)
    surface_data['comp_labels'] = texture

    # Plot for both views (lateral and medial)
    for view in ['lateral', 'medial']:
        fig, axes = plt.subplots(ncols=1, nrows=1, figsize=(7, 7), subplot_kw={'projection': '3d'})
        if hemisphere == 'left':
            plot_surf_left(surface_data['surf_mesh_left'], view, fig, axes, cmap=cmap, vmin=vmin, vmax=vmax, threshold=None, colorbar=False, darkness=darkness)
        else:
            plot_surf_right(surface_data['surf_mesh_right'], view, fig, axes, cmap=cmap, vmin=vmin, vmax=vmax, threshold=None, colorbar=False, darkness=darkness)
        plt.tight_layout()

# Set common parameters

darkness = .3

# # Plot for each hemisphere
# plot_brain_surface(color_rois(median_diffs), fsaverage.pial_left, 'left', cmap, vmin, vmax, darkness)
# plot_brain_surface(color_rois(median_diffs), fsaverage.pial_right, 'right', cmap, vmin, vmax, darkness)
