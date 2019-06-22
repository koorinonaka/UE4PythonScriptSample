import unreal
import sys

from utilities.asset_library import ProcessSlotTask, AssetStatics


class DeleteUnusedLocalDirectories(object):

    ignore_paths = ['/Game/Developers']  # Developersは除外

    def check_directory(self, directory):
        for ignore in self.ignore_paths:
            if directory.startswith(ignore):
                return

        if unreal.EditorAssetLibrary.does_directory_exist(directory):
            # get_assets_by_pathは/で終わる場合PackageNameとして認識しないので変換
            directory_name = unreal.Paths.normalize_directory_name(directory)
            if len(unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_path(directory_name, True)) == 0:
                # uassetではないアセットが存在する場合はDeleteに失敗する
                unreal.EditorAssetLibrary.delete_directory(directory)
                unreal.log('delete: {}'.format(directory.encode('utf-8')))

    def execute(self):
        search_path = "/Game/"
        try:
            search_path += sys.argv[1]
        except IndexError:
            pass

        if unreal.EditorAssetLibrary.does_directory_exist(search_path) != True:
            unreal.log_warning(
                'search directory is not found: {}'.format(search_path))
            return

        all_directories = filter(
            lambda x: x.endswith('/'),
            unreal.EditorAssetLibrary.list_assets(search_path, True, True)
        )

        ProcessSlotTask.execute(
            'checking directories',
            lambda x: self.check_directory(x),
            all_directories
        )


DeleteUnusedLocalDirectories().execute()
