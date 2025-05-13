import ftrack_api

# Твои персональные данные:
session = ftrack_api.Session(
    server_url='https://secondprize.ftrackapp.com',
    api_key='NTVjM2I1YTgtYjU3Mi00YWM2LThhNWItZDc2MjUwNjhiMGE5Ojo1MjJkNTQxYy05NWM1LTRhMjAtODVhNy1hYzYyNzY1MTJjMWU',
    api_user='second8prize@gmail.com'
)

def update_task_status(event):
    entity = event['data'].get('entity', {})
    changes = event['data'].get('changes', {})

    if not changes or 'statusid' not in changes:
        return

    version_id = entity.get('entityId')
    if not version_id:
        return

    try:
        version = session.query(f'AssetVersion where id is "{version_id}"').one()
        new_status = version['status']
        task = version['task']

        if task and new_status:
            task['status'] = new_status
            print(f"🔁 Task '{task['name']}' updated to status '{new_status['name']}' from version '{version['name']}'")
            session.commit()
    except Exception as e:
        print(f"⚠️ Error updating task status: {e}")

def main():
    session.event_hub.subscribe(
        'topic=entity.update and entityType=assetversion',
        update_task_status
    )
    print("✅ Listening for AssetVersion status updates...")

    session.event_hub.wait()

if __name__ == '__main__':
    main()
