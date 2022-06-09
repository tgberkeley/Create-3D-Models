import open3d as o3d
import copy

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp],
                                      zoom=0.4559,
                                      front=[0.6452, -0.3036, -0.7011],
                                      lookat=[1.9892, 2.0208, 1.8945],
                                      up=[-0.2779, -0.9482, 0.1556])

def execute_global_registration(source_down, target_down, source_fpfh,
                                target_fpfh, voxel_size):
    distance_threshold = voxel_size * 0.5
    print(":: RANSAC registration on downsampled point clouds.")
    print("   Since the downsampling voxel size is %.3f," % voxel_size)
    print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(True),
        3, [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold)
        ], o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999))
    return result

def execute_fast_global_registration(source_down, target_down, source_fpfh,
                                     target_fpfh, voxel_size):
    distance_threshold = voxel_size * 5
    print(":: Apply fast global registration with distance threshold %.3f" \
            % distance_threshold)
    result = o3d.pipelines.registration.registration_fast_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh,
        o3d.pipelines.registration.FastGlobalRegistrationOption(
            maximum_correspondence_distance=distance_threshold))
    return result

mesh_align = o3d.io.read_triangle_mesh("paratha_align.obj")
mesh_align.compute_vertex_normals()
mesh_align.translate(-mesh_align.get_center())
mesh_ref = o3d.io.read_triangle_mesh("paratha_ref.obj")
mesh_ref.compute_vertex_normals()
mesh_ref.translate(-mesh_ref.get_center())

scale = max(mesh_ref.get_axis_aligned_bounding_box().get_extent()) / max(mesh_align.get_axis_aligned_bounding_box().get_extent())
print('Scaling: ', scale)
mesh_align.scale(scale, center=mesh_align.get_center())

pcd_align = mesh_align.sample_points_poisson_disk(number_of_points=100000, init_factor=5)
voxel_size = max(mesh_ref.get_axis_aligned_bounding_box().get_extent())/512.0
print('Voxel size: ', voxel_size)
radius_feature = voxel_size * 5

pcd_fpfh_align = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_align,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
pcd_ref = mesh_ref.sample_points_poisson_disk(number_of_points=100000, init_factor=5)
pcd_fpfh_ref = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_ref,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))

result_ransac = execute_fast_global_registration(pcd_align, pcd_ref,
                                            pcd_fpfh_align, pcd_fpfh_ref,
                                            voxel_size)
#pcd_align.transform(result_ransac.transformation)

draw_registration_result(pcd_align, pcd_ref, result_ransac.transformation)

