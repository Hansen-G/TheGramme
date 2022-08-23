const GET_IMAGES = "session/GET_IMAGES";
const GET_IMAGE = "session/GET_IMAGE";
const ADD_IMAGE = "session/ADD_IMAGE";
const DELETE_IMAGE = "session/DELETE_IMAGE";
const EDIT_IMAGE = "session/EDIT_IMAGE";

const getImages = (images) => ({
	type: GET_IMAGES,
	images,
});

const getImage = (image) => ({
	type: GET_IMAGE,
	image,
});

const addImage = (image) => ({
	type: ADD_IMAGE,
	image,
});

const deleteImage = (id) => ({
	type: DELETE_IMAGE,
	id,
});

const editImage = (id) => ({
	type: EDIT_IMAGE,
	id,
});
// get images by user ID
// and get images by current user in profile page
export const loadImages = (id) => async (dispatch) => {
	const response = await fetch(`/api/images/users/${id}`);

	if (response.ok) {
		const data = await response.json();
		dispatch(getImages(data))
		return data;
	} else {
		return ["An error occurred. Please try again."];
	}
};
// create a image
// export const CreateImage =

const initialState = {};

export default function images(state = initialState, action) {
	let newState = {};
	switch (action.type) {
		case GET_IMAGES:
			newState = { ...action.images };
            return newState;
		// case ADD_IMAGE:

        default:
            return state
	}
}