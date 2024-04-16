from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='indxe')
    # path('', views.main_page, name='main page'),

    path('', views.profile_page, name='profile page'),
    path('profile/', views.profile_page, name='profile page'),
    path('galaxy_s10_profiledata/', views.galaxy_s10_profiledata, name='galaxy s10 profile data'),

    # Live Profile
    # Remove ProfileData
    path('live_profile_remove/', views.live_profile_remove, name='live profile remove'),

    # profile_record
    path('profile_record_write/', views.profile_record_write, name='profile record'),
    path('profile/profile_record_write/', views.profile_record_write, name='profile record'),
    path('profile_record_result/', views.profile_record_result, name='profile record result'),
    path('profile_record_table/', views.profile_record_table, name='profile record table'),

    # profile record CRUD =================================================================================================
    # profile record read
    path('profile_record_read/', views.profile_record_read, name='profile record read'),
    # profile_record_update
    path('profile_record_update/', views.profile_record_update, name='profile record update'),
    # profile_record_update_result
    path('profile_record_update_result/', views.profile_record_update_result, name='profile record update result'),
    # profile_record_delete
    path('profile_record_delete/', views.profile_record_delete, name='profile record delete'),

    # profile record chart
    path('profile_record_chart/', views.profile_record_chart, name='profile record chart'),
    # profile_record_chart_data
    path('profile_record_chart_FPS_data/', views.profile_record_chart_FPS_data, name='profile record chart data'),
    path('profile_record_chart_Memory_data/', views.profile_record_chart_Memory_data, name='profile record chart Memory data'),

    # profile_record_chart_Tris_data uri
    path('profile_record_chart_Tris_data/', views.profile_record_chart_Tris_data, name='profile record chart Tris data'),

    # profile_record_chart_Vertices_data uri
    path('profile_record_chart_Vertices_data/', views.profile_record_chart_Vertices_data, name='profile record chart Vertices data'),

    # profile_record_chart_DrawCall_data uri
    path('profile_record_chart_DrawCall_data/', views.profile_record_chart_DrawCall_data, name='profile record chart DrawCall data'),

    # profile_record_chart_SetPassCall_data uri
    path('profile_record_chart_SetPassCall_data/', views.profile_record_chart_SetPassCall_data, name='profile record chart SetPassCall data'),

    # profile_record_chart_TextureMemory_data uri
    path('profile_record_chart_TextureMemory_data/', views.profile_record_chart_TextureMemory_data, name='profile record chart TextureMemory data'),

    # profile_record_chart_MeshMemory_data uri
    path('profile_record_chart_MeshMemory_data/', views.profile_record_chart_MeshMemory_data, name='profile record chart MeshMemory data'),

    # ========================= donut chart ========================= #

    # profile_fps_donut_chart_data uri
    path('profile_fps_donut_chart_data/', views.profile_fps_donut_chart_data, name='profile fps donut chart data'),

    # profile_total_memory_donut_chart_data uri
    path('profile_total_memory_donut_chart_data/', views.profile_total_memory_donut_chart_data, name='profile total memory donut chart data'),

    # profile_tris_donut_chart_data uri
    path('profile_tris_donut_chart_data/', views.profile_tris_donut_chart_data, name='profile tris donut chart data'),

    # profile_vertices_donut_chart_data uri
    path('profile_vertices_donut_chart_data/', views.profile_vertices_donut_chart_data, name='profile vertices donut chart data'),

    # profile_texture_memory_donut_chart_data uri
    path('profile_texture_memory_donut_chart_data/', views.profile_texture_memory_donut_chart_data, name='profile texture memory donut chart data'),

    # profile_mesh_memory_donut_chart_data uri
    path('profile_mesh_memory_donut_chart_data/', views.profile_mesh_memory_donut_chart_data, name='profile mesh memory donut chart data'),

    # profile_draw_call_donut_chart_data uri
    path('profile_draw_call_donut_chart_data/', views.profile_draw_call_donut_chart_data, name='profile draw call donut chart data'),

    # profile_set_pass_call_donut_chart_data uri
    path('profile_set_pass_call_donut_chart_data/', views.profile_set_pass_call_donut_chart_data, name='profile set pass call donut chart data'),
]